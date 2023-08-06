# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, version 2.0 (the "License"); you may
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

""" Test Open message"""

import unittest
import netaddr
from yabgp.message.open import Open
from yabgp.common.constants import VERSION
from yabgp.common.constants import HDR_LEN


class TestOpen(unittest.TestCase):
    def setUp(self):
        self.open = Open()
        self.maxDiff = None

    def test_parse(self):
        msg_hex = b'\x04\x5b\xa0\x00\xb4\x03\x03\x03\x09\x25\x02\x06\x01\x04\x00\x01\x00\x80' \
                  b'\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02\x80\x00\x02\x02\x02\x00\x02\x03' \
                  b'\x83\x01\x00\x02\x06\x41\x04\x00\x01\x04\x6a'
        open_msg = self.open.parse(msg_hex)
        results = {'bgp_id': '3.3.3.9', 'version': 4, 'hold_time': 180, 'asn': 66666,
                   'capabilities': {
                       'cisco_multi_session': True,
                       'cisco_route_refresh': True,
                       'four_bytes_as': True,
                       'afi_safi': [(1, 128), (1, 1)],
                       'route_refresh': True}}
        self.assertEqual(results, open_msg)

    def test_construct(self):
        self.open.version = VERSION
        self.open.asn = 66666
        self.open.hold_time = 180
        self.open.bgp_id = int(netaddr.IPAddress('1.1.1.1'))
        my_capa = {
            'graceful_restart': False,
            'cisco_multi_session': True,
            'cisco_route_refresh': True,
            'four_bytes_as': True,
            'afi_safi': [(1, 128), (1, 1)],
            'route_refresh': True}
        msg_hex = self.open.construct(my_capa)
        hope_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00=\x01\x04[\xa0\x00\xb4\x01' \
                   b'\x01\x01\x01 \x02\x06\x01\x04\x00\x01\x00\x80\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02\x80\x00' \
                   b'\x02\x02\x02\x00\x02\x06A\x04\x00\x01\x04j'
        self.assertEqual(hope_hex, msg_hex)

    def test_construct_add_path(self):
        self.open.version = VERSION
        self.open.asn = 64512
        self.open.hold_time = 180
        self.open.bgp_id = int(netaddr.IPAddress('10.0.0.6'))
        my_capa = {
            'cisco_route_refresh': True,
            'route_refresh': True,
            'add_path': 'ipv4_receive',
            'four_bytes_as': True,
            'afi_safi': [(1, 1)],
            'enhanced_route_refresh': True}
        msg_hex = self.open.construct(my_capa)
        hope_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00A\x01\x04' \
                   b'\xfc\x00\x00\xb4\n\x00\x00\x06$\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02\x80' \
                   b'\x00\x02\x02\x02\x00\x02\x06A\x04\x00\x00\xfc\x00\x02\x06E\x04\x00\x01\x01\x01\x02\x02F\x00'

        self.assertEqual(hope_hex, msg_hex)

    def test_parser_add_path(self):
        msg_hex = b'\x04\xfc\x00\x00\xb4\x0a\x00\x00\x06\x24\x02\x06\x01\x04\x00\x01\x00\x01\x02\x02\x80\x00\x02' \
                  b'\x02\x02\x00\x02\x02\x46\x00\x02\x06\x45\x04\x00\x01\x01\x03\x02\x06\x41\x04\x00\x00\xfc\x00'
        open_msg = self.open.parse(msg_hex)
        results = {
            'bgp_id': '10.0.0.6',
            'version': 4,
            'hold_time': 180,
            'asn': 64512,
            'capabilities': {
                'cisco_route_refresh': True,
                'route_refresh': True,
                'add_path': [{'afi_safi': 'ipv4', 'send/receive': 'both'}],
                'four_bytes_as': True,
                'afi_safi': [(1, 1)],
                'enhanced_route_refresh': True}}
        self.assertEqual(results, open_msg)

    def test_parse_llgr(self):
        msg_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x4e\x01' \
                  b'\x04\x01\x2c\x00\xb4\x03\x03\x03\x03\x31\x02\x06\x01\x04\x00\x01\x00\x01\x02' \
                  b'\x06\x01\x04\x00\x01\x00\x85\x02\x02\x80\x00\x02\x02\x02\x00\x02\x06\x41\x04' \
                  b'\x00\x00\x01\x2c\x02\x04\x40\x02\x80\x78\x02\x09\x47\x07\x00\x01\x85\x80\x00\x01\x68'
        results = {
            'asn': 300,
            'bgp_id': '3.3.3.3',
            'capabilities': {
                'LLGR': [{'afi_safi': [1, 133], 'time': 360}],
                'afi_safi': [(1, 1), (1, 133)],
                'cisco_route_refresh': True,
                'four_bytes_as': True,
                'graceful_restart': True,
                'route_refresh': True},
            'hold_time': 180,
            'version': 4}
        self.assertEqual(results, self.open.parse(msg_hex[HDR_LEN:]))

    def test_parse_add_path_llgr(self):
        msg_hex = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' \
                  b'\x00\x41\x01\x04\xfd\xe9\x00\xb4\x0a\x00\x00\x07\x24\x02\x22\x01' \
                  b'\x04\x00\x01\x00\x01\x01\x04\x00\x01\x00\x04\x02\x00\x40\x02\x01' \
                  b'\x2c\x41\x04\x00\x00\xfd\xe9\x45\x08\x00\x01\x01\x01\x00\x01\x04\x01'
        results = {
            'asn': 65001,
            'bgp_id': '10.0.0.7',
            'capabilities': {
                'add_path': [
                    {'afi_safi': 'ipv4', 'send/receive': 'receive'},
                    {'afi_safi': 'ipv4_lu', 'send/receive': 'receive'}],
                'afi_safi': [(1, 1), (1, 4)],
                'four_bytes_as': True,
                'graceful_restart': True,
                'route_refresh': True},
            'hold_time': 180,
            'version': 4
        }
        self.assertEqual(results, self.open.parse(msg_hex[HDR_LEN:]))


if __name__ == '__main__':
    unittest.main()
