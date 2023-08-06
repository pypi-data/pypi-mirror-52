# Copyright (c) 2007 by Mark Bergsma <mark@nedworks.org>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Twisted Factory, BGP implementation.
"""

import logging
import socket
import platform
import struct
import sys

import netaddr
from twisted.internet import protocol
from twisted.internet import reactor
from oslo_config import cfg

from yabgp.core.protocol import BGP
from yabgp.core.fsm import FSM
from yabgp.common import constants as bgp_cons
from yabgp.common.afn import AFNUM_INET

LOG = logging.getLogger(__name__)

CONF = cfg.CONF


class BGPFactory(protocol.Factory):
    """Base factory for creating BGP protocol instances."""

    protocol = BGP
    FSM = FSM

    def buildProtocol(self, addr):
        """Builds a BGPProtocol instance.

        :param addr : address used for buliding protocol.
        """
        return protocol.Factory.buildProtocol(self, addr)

    def startedConnecting(self, connector):
        """Called when a connection attempt has been initiated.

        :param connector : Twisted connector
        """
        pass

    def clientConnectionLost(self, connector, reason):
        """ Called when a TCP client connection was lost.

        :param connector : Twisted connector
        :param reason : connection faied reason.
        """
        LOG.info("Client connection lost:%s", reason.getErrorMessage())


class BGPPeering(BGPFactory):
    """Class managing a BGP session with a peer.
    One connection, One BGPPeering class.
    """

    def __init__(self, myasn=None, myaddr=None, peerasn=None, peeraddr=None,
                 afisafi=None, md5=None, handler=None):
        """Initial a BGPPeering instance.

        :param myasn: local bgp as number.
        :param myaddr: local ip address.
        :param peerasn: remote bgp peer as number
        :param peeraddr: remote peer ip address.
        :param msgpath: the path to store bgp message file.
        :param afisafi: afi and safi
        :param md5: TCP md5 string
        """
        LOG.info('Init BGPPeering for peer %s', peeraddr)
        self.my_asn = myasn
        self.my_addr = myaddr
        self.peer_addr = peeraddr
        self.peer_id = None
        self.bgp_id = None
        self.peer_asn = peerasn
        self.afi_safi = afisafi
        self.md5 = md5

        self.status = False
        self.fsm = BGPFactory.FSM(self)
        self.handler = handler

        # reference to the BGPProtocol instance in ESTAB state
        self.estab_protocol = None

    def buildProtocol(self, addr):

        """Builds a BGP protocol instance

        :param addr: IP address used for building protocol.
        """
        LOG.info("[%s]Building a new BGP protocol instance", self.peer_addr)

        p = BGPFactory.buildProtocol(self, addr)
        if p is not None:
            self._initProtocol(p, addr)
        self.estab_protocol = p
        return p

    def _initProtocol(self, protocol, addr):

        """Initializes a BGPProtocol instance

        :param protocol: twisted Protocol
        :param addr: ip address
        """

        protocol.bgp_peering = self

        # Hand over the FSM
        protocol.fsm = self.fsm
        protocol.fsm.protocol = protocol

        if addr.port == bgp_cons.PORT:
            protocol.fsm.state = bgp_cons.ST_CONNECT
        else:
            protocol.fsm.state = bgp_cons.ST_ACTIVE

    def clientConnectionFailed(self, connector, reason):

        """Called when the outgoing connection failed.

        :param connector: Twisted connector
        :param reason: connection failed reason
        """

        error_msg = "[%s]Client connection failed: %s" % (self.peer_addr, reason.getErrorMessage())
        self.handler.on_connection_failed(self.peer_addr, reason.getErrorMessage())
        LOG.info(error_msg)
        # There is no protocol instance yet at this point.
        # Catch a possible NotificationException
        try:
            self.fsm.connection_failed()
        except Exception as e:
            LOG.info("[%s]Client connection failed: %s", self.peer_addr, e)

    def automatic_start(self, idle_hold=False):

        """BGP AutomaticStart event (event 3)

        :param idle_hold: flag represents used Idle Hold
        """
        if self.fsm.state == bgp_cons.ST_IDLE:
            if self.fsm.automatic_start(idle_hold):
                self.status = True
                # Create outbound connection as a client
                self.connect()

    def manual_start(self, idle_hold=False):
        if self.fsm.state == bgp_cons.ST_ESTABLISHED:
            return "EST"
        elif self.fsm.state == bgp_cons.ST_IDLE:
            if self.fsm.manual_start(idle_hold=idle_hold):
                self.status = True
                self.connect()
                return True
        else:
            return False

    def manual_stop(self):

        """BGP ManualStop event (event 2) Returns a DeferredList that
        will fire once the connection(s) have closed"""

        return self.fsm.manual_stop()

    def connection_closed(self, pro, disconnect=False):
        """
        Called by FSM or Protocol when the BGP connection has been closed.

        :param pro: twisted protocol
        :param disconnect: the status of connection
        """

        LOG.info("[%s]Connection closed", self.peer_addr)
        if pro is not None:
            # Connection succeeded previously, protocol exists
            # Remove the protocol, if it exists
            if pro is self.estab_protocol:
                self.estab_protocol = None
                # self.fsm should still be valid and set to ST_IDLE
                self.fsm.state = bgp_cons.ST_IDLE

        if self.fsm.allow_automatic_start:
            self.automatic_start(idle_hold=True)

    def connect_retry(self):

        """Called by FSM when we should reattempt to connect.
        """
        try:
            self.connect()
        except Exception as e:
            LOG.error(e)
            import traceback
            LOG.debug(traceback.format_exc())

    def set_peer_id(self, bgp_id):
        """
        Should be called when an Open message was received from a peer.
        Sets the BGP identifier of the peer if it wasn't set yet. If the
        new peer id is unequal to the existing one, CEASE all connections.
        s
        :param bgp_id: BGP ID
        """

        if self.peer_id is None:
            self.peer_id = bgp_id
            LOG.info('Set BGP peer id %s', bgp_id)
        elif self.peer_id != bgp_id:
            # Ouch, schizophrenia. The BGP id of the peer is unequal to
            # the ids of current and/or previous sessions. Close all
            # connections.
            self.peer_id = None

    def connect(self):

        """Initiates a TCP client connection to the peer. Should only be called from
        BGPPeering or FSM, otherwise use manualStart() instead.
        """
        # DEBUG
        LOG.info("(Re)connect to %s", self.peer_addr)

        if self.fsm.state != bgp_cons.ST_ESTABLISHED:

            connector = reactor.connectTCP(
                host=self.peer_addr,
                port=bgp_cons.PORT,
                factory=self,
                timeout=30,
                bindAddress=(self.my_addr, 0))
            if isinstance(self.md5, str) and self.md5:
                md5sig = self.get_tcp_md5sig(self.md5, self.peer_addr, bgp_cons.PORT)
                if md5sig:
                    connector.transport.getHandle().setsockopt(
                        socket.IPPROTO_TCP, bgp_cons.TCP_MD5SIG, md5sig)
                else:
                    sys.exit()
            return True
        else:
            return False

    @staticmethod
    def get_tcp_md5sig(md5_str, host, port):
        """set tcp md5
        """
        os_type = platform.system()
        if os_type != 'Linux':
            LOG.error('YABGP has no MD5 support for %s', os_type)
            return None

        # address family
        if netaddr.IPAddress(host).version == 4:
            # ipv4 address
            afi = AFNUM_INET
        elif netaddr.IPAddress(host).version == 6:
            # ipv6 address
            LOG.error("Does not support ipv6 address family")
            sys.exit()
        else:
            afi = None
            LOG.error('Peer address is not a valid ipv4/ipv6 address')
        try:
            n_port = socket.htons(port)
            if afi == AFNUM_INET:
                n_addr = socket.inet_pton(socket.AF_INET, host)
                tcp_md5sig = 'HH4s%dx2xH4x%ds' % (
                    bgp_cons.SS_PADSIZE_IPV4, bgp_cons.TCP_MD5SIG_MAXKEYLEN)
                md5sig = struct.pack(
                    tcp_md5sig, socket.AF_INET, n_port, n_addr, len(md5_str), md5_str.encode())
                return md5sig
            else:
                return None
        except socket.error as e:
            LOG.error('This linux machine does not support TCP_MD5SIG: (%s)', str(e))
            return None
