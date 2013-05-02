#!/usr/bin/env python
# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.
import unittest

try:
    import loxi.of10 as ofp
    from loxi.generic_util import OFReader
except ImportError:
    exit("loxi package not found. Try setting PYTHONPATH.")

class TestImports(unittest.TestCase):
    def test_toplevel(self):
        import loxi
        self.assertTrue(hasattr(loxi, "ProtocolError"))
        self.assertEquals(loxi.version_names[1], "1.0")
        ofp = loxi.protocol(1)
        self.assertEquals(ofp.OFP_VERSION, 1)
        self.assertTrue(hasattr(ofp, "action"))
        self.assertTrue(hasattr(ofp, "common"))
        self.assertTrue(hasattr(ofp, "const"))
        self.assertTrue(hasattr(ofp, "message"))

    def test_version(self):
        import loxi
        self.assertTrue(hasattr(loxi.of10, "ProtocolError"))
        self.assertTrue(hasattr(loxi.of10, "OFP_VERSION"))
        self.assertEquals(loxi.of10.OFP_VERSION, 1)
        self.assertTrue(hasattr(loxi.of10, "action"))
        self.assertTrue(hasattr(loxi.of10, "common"))
        self.assertTrue(hasattr(loxi.of10, "const"))
        self.assertTrue(hasattr(loxi.of10, "message"))

class TestActions(unittest.TestCase):
    def test_output_pack(self):
        expected = "\x00\x00\x00\x08\xff\xf8\xff\xff"
        action = ofp.action.output(port=ofp.OFPP_IN_PORT, max_len=0xffff)
        self.assertEquals(expected, action.pack())

    def test_output_unpack(self):
        # Normal case
        buf = "\x00\x00\x00\x08\xff\xf8\xff\xff"
        action = ofp.action.output.unpack(buf)
        self.assertEqual(action.port, ofp.OFPP_IN_PORT)
        self.assertEqual(action.max_len, 0xffff)

        # Invalid length
        #buf = "\x00\x00\x00\x09\xff\xf8\xff\xff\x00"
        #with self.assertRaises(ofp.ProtocolError):
        #    ofp.action.output.unpack(buf)

    def test_output_equality(self):
        action = ofp.action.output(port=1, max_len=0x1234)
        action2 = ofp.action.output(port=1, max_len=0x1234)
        self.assertEquals(action, action2)

        action2.port = 2
        self.assertNotEquals(action, action2)
        action2.port = 1

        action2.max_len = 0xffff
        self.assertNotEquals(action, action2)
        action2.max_len = 0x1234

    def test_output_show(self):
        action = ofp.action.output(port=1, max_len=0x1234)
        expected = "output { port = 1, max_len = 0x1234 }"
        self.assertEquals(expected, action.show())

    def test_bsn_set_tunnel_dst_pack(self):
        expected = ''.join([
            "\xff\xff", "\x00\x10", # type/length
            "\x00\x5c\x16\xc7", # experimenter
            "\x00\x00\x00\x02", # subtype
            "\x12\x34\x56\x78" # dst
        ])
        action = ofp.action.bsn_set_tunnel_dst(dst=0x12345678)
        self.assertEquals(expected, action.pack())

    def test_bsn_set_tunnel_dst_unpack(self):
        buf = ''.join([
            "\xff\xff", "\x00\x10", # type/length
            "\x00\x5c\x16\xc7", # experimenter
            "\x00\x00\x00\x02", # subtype
            "\x12\x34\x56\x78" # dst
        ])
        action = ofp.action.bsn_set_tunnel_dst.unpack(buf)
        self.assertEqual(action.subtype, 2)
        self.assertEqual(action.dst, 0x12345678)

# Assumes action serialization/deserialization works
class TestActionList(unittest.TestCase):
    def test_normal(self):
        expected = []
        bufs = []

        def add(action):
            expected.append(action)
            bufs.append(action.pack())

        add(ofp.action.output(port=1, max_len=0xffff))
        add(ofp.action.output(port=2, max_len=0xffff))
        add(ofp.action.output(port=ofp.OFPP_IN_PORT, max_len=0xffff))
        add(ofp.action.bsn_set_tunnel_dst(dst=0x12345678))
        add(ofp.action.nicira_dec_ttl())

        actions = ofp.action.unpack_list(OFReader(''.join(bufs)))
        self.assertEquals(actions, expected)

    def test_empty_list(self):
        self.assertEquals(ofp.action.unpack_list(OFReader('')), [])

    def test_invalid_list_length(self):
        buf = '\x00' * 9
        with self.assertRaisesRegexp(ofp.ProtocolError, 'Buffer too short'):
            ofp.action.unpack_list(OFReader(buf))

    def test_invalid_action_length(self):
        buf = '\x00' * 8
        with self.assertRaisesRegexp(ofp.ProtocolError, 'Buffer too short'):
            ofp.action.unpack_list(OFReader(buf))

        buf = '\x00\x00\x00\x04'
        with self.assertRaisesRegexp(ofp.ProtocolError, 'Buffer too short'):
            ofp.action.unpack_list(OFReader(buf))

        buf = '\x00\x00\x00\x10\x00\x00\x00\x00'
        with self.assertRaisesRegexp(ofp.ProtocolError, 'Buffer too short'):
            ofp.action.unpack_list(OFReader(buf))

    def test_invalid_action_type(self):
        buf = '\xff\xfe\x00\x08\x00\x00\x00\x00'
        with self.assertRaisesRegexp(ofp.ProtocolError, 'unknown action type'):
            ofp.action.unpack_list(OFReader(buf))

class TestConstants(unittest.TestCase):
    def test_ports(self):
        self.assertEquals(0xffff, ofp.OFPP_NONE)

    def test_wildcards(self):
        self.assertEquals(0xfc000, ofp.OFPFW_NW_DST_MASK)

class TestCommon(unittest.TestCase):
    def test_port_desc_pack(self):
        obj = ofp.port_desc(port_no=ofp.OFPP_CONTROLLER,
                            hw_addr=[1,2,3,4,5,6],
                            name="foo",
                            config=ofp.OFPPC_NO_FLOOD,
                            state=ofp.OFPPS_STP_FORWARD,
                            curr=ofp.OFPPF_10MB_HD,
                            advertised=ofp.OFPPF_1GB_FD,
                            supported=ofp.OFPPF_AUTONEG,
                            peer=ofp.OFPPF_PAUSE_ASYM)
        expected = ''.join([
            '\xff\xfd', # port_no
            '\x01\x02\x03\x04\x05\x06', # hw_addr
            'foo'.ljust(16, '\x00'), # name
            '\x00\x00\x00\x10', # config
            '\x00\x00\x02\x00', # state
            '\x00\x00\x00\x01', # curr
            '\x00\x00\x00\x20', # advertised
            '\x00\x00\x02\x00', # supported
            '\x00\x00\x08\x00', # peer
        ])
        self.assertEquals(expected, obj.pack())

    def test_port_desc_unpack(self):
        buf = ''.join([
            '\xff\xfd', # port_no
            '\x01\x02\x03\x04\x05\x06', # hw_addr
            'foo'.ljust(16, '\x00'), # name
            '\x00\x00\x00\x10', # config
            '\x00\x00\x02\x00', # state
            '\x00\x00\x00\x01', # curr
            '\x00\x00\x00\x20', # advertised
            '\x00\x00\x02\x00', # supported
            '\x00\x00\x08\x00', # peer
        ])
        obj = ofp.port_desc.unpack(buf)
        self.assertEquals(ofp.OFPP_CONTROLLER, obj.port_no)
        self.assertEquals('foo', obj.name)
        self.assertEquals(ofp.OFPPF_PAUSE_ASYM, obj.peer)

    def test_table_stats_entry_pack(self):
        obj = ofp.table_stats_entry(table_id=3,
                                    name="foo",
                                    wildcards=ofp.OFPFW_ALL,
                                    max_entries=5,
                                    active_count=2,
                                    lookup_count=1099511627775,
                                    matched_count=9300233470495232273L)
        expected = ''.join([
            '\x03', # table_id
            '\x00\x00\x00', # pad
            'foo'.ljust(32, '\x00'), # name
            '\x00\x3f\xFF\xFF', # wildcards
            '\x00\x00\x00\x05', # max_entries
            '\x00\x00\x00\x02', # active_count
            '\x00\x00\x00\xff\xff\xff\xff\xff', # lookup_count
            '\x81\x11\x11\x11\x11\x11\x11\x11', # matched_count
        ])
        self.assertEquals(expected, obj.pack())

    def test_table_stats_entry_unpack(self):
        buf = ''.join([
            '\x03', # table_id
            '\x00\x00\x00', # pad
            'foo'.ljust(32, '\x00'), # name
            '\x00\x3f\xFF\xFF', # wildcards
            '\x00\x00\x00\x05', # max_entries
            '\x00\x00\x00\x02', # active_count
            '\x00\x00\x00\xff\xff\xff\xff\xff', # lookup_count
            '\x81\x11\x11\x11\x11\x11\x11\x11', # matched_count
        ])
        obj = ofp.table_stats_entry.unpack(buf)
        self.assertEquals(3, obj.table_id)
        self.assertEquals('foo', obj.name)
        self.assertEquals(9300233470495232273L, obj.matched_count)

    def test_flow_stats_entry_pack(self):
        obj = ofp.flow_stats_entry(table_id=3,
                                   match=ofp.match(),
                                   duration_sec=1,
                                   duration_nsec=2,
                                   priority=100,
                                   idle_timeout=5,
                                   hard_timeout=10,
                                   cookie=0x0123456789abcdef,
                                   packet_count=10,
                                   byte_count=1000,
                                   actions=[ofp.action.output(port=1),
                                            ofp.action.output(port=2)])
        expected = ''.join([
            '\x00\x68', # length
            '\x03', # table_id
            '\x00', # pad
            '\x00\x3f\xff\xff', # match.wildcards
            '\x00' * 36, # remaining match fields
            '\x00\x00\x00\x01', # duration_sec
            '\x00\x00\x00\x02', # duration_nsec
            '\x00\x64', # priority
            '\x00\x05', # idle_timeout
            '\x00\x0a', # hard_timeout
            '\x00' * 6, # pad2
            '\x01\x23\x45\x67\x89\xab\xcd\xef', # cookie
            '\x00\x00\x00\x00\x00\x00\x00\x0a', # packet_count
            '\x00\x00\x00\x00\x00\x00\x03\xe8', # byte_count
            '\x00\x00', # actions[0].type
            '\x00\x08', # actions[0].len
            '\x00\x01', # actions[0].port
            '\x00\x00', # actions[0].max_len
            '\x00\x00', # actions[1].type
            '\x00\x08', # actions[1].len
            '\x00\x02', # actions[1].port
            '\x00\x00', # actions[1].max_len
        ])
        self.assertEquals(expected, obj.pack())

    def test_flow_stats_entry_unpack(self):
        buf = ''.join([
            '\x00\x68', # length
            '\x03', # table_id
            '\x00', # pad
            '\x00\x3f\xff\xff', # match.wildcards
            '\x00' * 36, # remaining match fields
            '\x00\x00\x00\x01', # duration_sec
            '\x00\x00\x00\x02', # duration_nsec
            '\x00\x64', # priority
            '\x00\x05', # idle_timeout
            '\x00\x0a', # hard_timeout
            '\x00' * 6, # pad2
            '\x01\x23\x45\x67\x89\xab\xcd\xef', # cookie
            '\x00\x00\x00\x00\x00\x00\x00\x0a', # packet_count
            '\x00\x00\x00\x00\x00\x00\x03\xe8', # byte_count
            '\x00\x00', # actions[0].type
            '\x00\x08', # actions[0].len
            '\x00\x01', # actions[0].port
            '\x00\x00', # actions[0].max_len
            '\x00\x00', # actions[1].type
            '\x00\x08', # actions[1].len
            '\x00\x02', # actions[1].port
            '\x00\x00', # actions[1].max_len
        ])
        obj = ofp.flow_stats_entry.unpack(buf)
        self.assertEquals(3, obj.table_id)
        self.assertEquals(ofp.OFPFW_ALL, obj.match.wildcards)
        self.assertEquals(2, len(obj.actions))
        self.assertEquals(1, obj.actions[0].port)
        self.assertEquals(2, obj.actions[1].port)

    def test_match(self):
        match = ofp.match()
        self.assertEquals(match.wildcards, ofp.OFPFW_ALL)
        self.assertEquals(match.tcp_src, 0)
        buf = match.pack()
        match2 = ofp.match.unpack(buf)
        self.assertEquals(match, match2)

class TestMessages(unittest.TestCase):
    def test_hello_construction(self):
        msg = ofp.message.hello()
        self.assertEquals(msg.version, ofp.OFP_VERSION)
        self.assertEquals(msg.type, ofp.OFPT_HELLO)
        self.assertEquals(msg.xid, None)

        msg = ofp.message.hello(xid=123)
        self.assertEquals(msg.xid, 123)

        # 0 is a valid xid distinct from None
        msg = ofp.message.hello(xid=0)
        self.assertEquals(msg.xid, 0)

    def test_hello_unpack(self):
        # Normal case
        buf = "\x01\x00\x00\x08\x12\x34\x56\x78"
        msg = ofp.message.hello(xid=0x12345678)
        self.assertEquals(buf, msg.pack())

        # Invalid length
        #buf = "\x01\x00\x00\x09\x12\x34\x56\x78\x9a"
        #with self.assertRaisesRegexp(ofp.ProtocolError, "should be 8"):
        #    ofp.message.hello.unpack(buf)

    def test_echo_request_construction(self):
        msg = ofp.message.echo_request(data="abc")
        self.assertEquals(msg.data, "abc")

    def test_echo_request_pack(self):
        msg = ofp.message.echo_request(xid=0x12345678, data="abc")
        buf = msg.pack()
        self.assertEquals(buf, "\x01\x02\x00\x0b\x12\x34\x56\x78\x61\x62\x63")

        msg2 = ofp.message.echo_request.unpack(buf)
        self.assertEquals(msg, msg2)

    def test_echo_request_unpack(self):
        # Normal case
        buf = "\x01\x02\x00\x0b\x12\x34\x56\x78\x61\x62\x63"
        msg = ofp.message.echo_request(xid=0x12345678, data="abc")
        self.assertEquals(buf, msg.pack())

        # Invalid length
        buf = "\x01\x02\x00\x07\x12\x34\x56"
        with self.assertRaisesRegexp(ofp.ProtocolError, "buffer too short"):
            ofp.message.echo_request.unpack(buf)

    def test_echo_request_equality(self):
        msg = ofp.message.echo_request(xid=0x12345678, data="abc")
        msg2 = ofp.message.echo_request(xid=0x12345678, data="abc")
        #msg2 = ofp.message.echo_request.unpack(msg.pack())
        self.assertEquals(msg, msg2)

        msg2.xid = 1
        self.assertNotEquals(msg, msg2)
        msg2.xid = msg.xid

        msg2.data = "a"
        self.assertNotEquals(msg, msg2)
        msg2.data = msg.data

    def test_echo_request_show(self):
        expected = "echo_request { xid = 0x12345678, data = 'ab\\x01' }"
        msg = ofp.message.echo_request(xid=0x12345678, data="ab\x01")
        self.assertEquals(msg.show(), expected)

    def test_flow_add(self):
        match = ofp.match()
        msg = ofp.message.flow_add(xid=1,
                                   match=match,
                                   cookie=1,
                                   idle_timeout=5,
                                   flags=ofp.OFPFF_CHECK_OVERLAP,
                                   actions=[
                                       ofp.action.output(port=1),
                                       ofp.action.output(port=2),
                                       ofp.action.output(port=ofp.OFPP_CONTROLLER,
                                                         max_len=1024)])
        buf = msg.pack()
        msg2 = ofp.message.flow_add.unpack(buf)
        self.assertEquals(msg, msg2)

    def test_port_mod_pack(self):
        msg = ofp.message.port_mod(xid=2,
                                   port_no=ofp.OFPP_CONTROLLER,
                                   hw_addr=[1,2,3,4,5,6],
                                   config=0x90ABCDEF,
                                   mask=0xFF11FF11,
                                   advertise=0xCAFE6789)
        expected = "\x01\x0f\x00\x20\x00\x00\x00\x02\xff\xfd\x01\x02\x03\x04\x05\x06\x90\xab\xcd\xef\xff\x11\xff\x11\xca\xfe\x67\x89\x00\x00\x00\x00"
        self.assertEquals(expected, msg.pack())

    def test_desc_stats_reply_pack(self):
        msg = ofp.message.desc_stats_reply(xid=3,
                                           flags=ofp.OFPSF_REPLY_MORE,
                                           mfr_desc="The Indigo-2 Community",
                                           hw_desc="Unknown server",
                                           sw_desc="Indigo-2 LRI pre-release",
                                           serial_num="11235813213455",
                                           dp_desc="Indigo-2 LRI forwarding module")
        expected = ''.join([
            '\x01', '\x11', # version/type
            '\x04\x2c', # length
            '\x00\x00\x00\x03', # xid
            '\x00\x00', # stats_type
            '\x00\x01', # flags
            'The Indigo-2 Community'.ljust(256, '\x00'), # mfr_desc
            'Unknown server'.ljust(256, '\x00'), # hw_desc
            'Indigo-2 LRI pre-release'.ljust(256, '\x00'), # sw_desc
            '11235813213455'.ljust(32, '\x00'), # serial_num
            'Indigo-2 LRI forwarding module'.ljust(256, '\x00'), # dp_desc
        ])
        self.assertEquals(expected, msg.pack())

    def test_desc_stats_reply_unpack(self):
        buf = ''.join([
            '\x01', '\x11', # version/type
            '\x04\x2c', # length
            '\x00\x00\x00\x03', # xid
            '\x00\x00', # stats_type
            '\x00\x01', # flags
            'The Indigo-2 Community'.ljust(256, '\x00'), # mfr_desc
            'Unknown server'.ljust(256, '\x00'), # hw_desc
            'Indigo-2 LRI pre-release'.ljust(256, '\x00'), # sw_desc
            '11235813213455'.ljust(32, '\x00'), # serial_num
            'Indigo-2 LRI forwarding module'.ljust(256, '\x00'), # dp_desc
        ])
        msg = ofp.message.desc_stats_reply.unpack(buf)
        self.assertEquals('Indigo-2 LRI forwarding module', msg.dp_desc)
        self.assertEquals('11235813213455', msg.serial_num)
        self.assertEquals(ofp.OFPST_DESC, msg.stats_type)
        self.assertEquals(ofp.OFPSF_REPLY_MORE, msg.flags)

    def test_port_status_pack(self):
        desc = ofp.port_desc(port_no=ofp.OFPP_CONTROLLER,
                             hw_addr=[1,2,3,4,5,6],
                             name="foo",
                             config=ofp.OFPPC_NO_FLOOD,
                             state=ofp.OFPPS_STP_FORWARD,
                             curr=ofp.OFPPF_10MB_HD,
                             advertised=ofp.OFPPF_1GB_FD,
                             supported=ofp.OFPPF_AUTONEG,
                             peer=ofp.OFPPF_PAUSE_ASYM)

        msg = ofp.message.port_status(xid=4,
                                      reason=ofp.OFPPR_DELETE,
                                      desc=desc)
        expected = ''.join([
            '\x01', '\x0c', # version/type
            '\x00\x40', # length
            '\x00\x00\x00\x04', # xid
            '\x01', # reason
            '\x00\x00\x00\x00\x00\x00\x00' # pad
            '\xff\xfd', # desc.port_no
            '\x01\x02\x03\x04\x05\x06', # desc.hw_addr
            'foo'.ljust(16, '\x00'), # desc.name
            '\x00\x00\x00\x10', # desc.config
            '\x00\x00\x02\x00', # desc.state
            '\x00\x00\x00\x01', # desc.curr
            '\x00\x00\x00\x20', # desc.advertised
            '\x00\x00\x02\x00', # desc.supported
            '\x00\x00\x08\x00', # desc.peer
        ])
        self.assertEquals(expected, msg.pack())

    def test_port_status_unpack(self):
        buf = ''.join([
            '\x01', '\x0c', # version/type
            '\x00\x40', # length
            '\x00\x00\x00\x04', # xid
            '\x01', # reason
            '\x00\x00\x00\x00\x00\x00\x00' # pad
            '\xff\xfd', # desc.port_no
            '\x01\x02\x03\x04\x05\x06', # desc.hw_addr
            'foo'.ljust(16, '\x00'), # desc.name
            '\x00\x00\x00\x10', # desc.config
            '\x00\x00\x02\x00', # desc.state
            '\x00\x00\x00\x01', # desc.curr
            '\x00\x00\x00\x20', # desc.advertised
            '\x00\x00\x02\x00', # desc.supported
            '\x00\x00\x08\x00', # desc.peer
        ])
        msg = ofp.message.port_status.unpack(buf)
        self.assertEquals('foo', msg.desc.name)
        self.assertEquals(ofp.OFPPF_PAUSE_ASYM, msg.desc.peer)

    def test_port_stats_reply_pack(self):
        msg = ofp.message.port_stats_reply(xid=5, flags=0, entries=[
            ofp.port_stats_entry(port_no=1, rx_packets=56, collisions=5),
            ofp.port_stats_entry(port_no=ofp.OFPP_LOCAL, rx_packets=1, collisions=1)])
        expected = ''.join([
            '\x01', '\x11', # version/type
            '\x00\xdc', # length
            '\x00\x00\x00\x05', # xid
            '\x00\x04', # stats_type
            '\x00\x00', # flags
            '\x00\x01', # entries[0].port_no
            '\x00\x00\x00\x00\x00\x00' # entries[0].pad
            '\x00\x00\x00\x00\x00\x00\x00\x38', # entries[0].rx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_frame_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_over_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_crc_err
            '\x00\x00\x00\x00\x00\x00\x00\x05', # entries[0].collisions
            '\xff\xfe', # entries[1].port_no
            '\x00\x00\x00\x00\x00\x00' # entries[1].pad
            '\x00\x00\x00\x00\x00\x00\x00\x01', # entries[1].rx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_frame_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_over_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_crc_err
            '\x00\x00\x00\x00\x00\x00\x00\x01', # entries[1].collisions
        ])
        self.assertEquals(expected, msg.pack())

    def test_port_stats_reply_unpack(self):
        buf = ''.join([
            '\x01', '\x11', # version/type
            '\x00\xdc', # length
            '\x00\x00\x00\x05', # xid
            '\x00\x04', # stats_type
            '\x00\x00', # flags
            '\x00\x01', # entries[0].port_no
            '\x00\x00\x00\x00\x00\x00' # entries[0].pad
            '\x00\x00\x00\x00\x00\x00\x00\x38', # entries[0].rx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].tx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_frame_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_over_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[0].rx_crc_err
            '\x00\x00\x00\x00\x00\x00\x00\x05', # entries[0].collisions
            '\xff\xfe', # entries[1].port_no
            '\x00\x00\x00\x00\x00\x00' # entries[1].pad
            '\x00\x00\x00\x00\x00\x00\x00\x01', # entries[1].rx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_packets
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_bytes
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_dropped
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].tx_errors
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_frame_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_over_err
            '\x00\x00\x00\x00\x00\x00\x00\x00', # entries[1].rx_crc_err
            '\x00\x00\x00\x00\x00\x00\x00\x01', # entries[1].collisions
        ])
        msg = ofp.message.port_stats_reply.unpack(buf)
        self.assertEquals(ofp.OFPST_PORT, msg.stats_type)
        self.assertEquals(2, len(msg.entries))

    sample_flow_stats_reply_buf = ''.join([
        '\x01', '\x11', # version/type
        '\x00\xe4', # length
        '\x00\x00\x00\x06', # xid
        '\x00\x01', # stats_type
        '\x00\x00', # flags
        '\x00\x68', # entries[0].length
        '\x03', # entries[0].table_id
        '\x00', # entries[0].pad
        '\x00\x3f\xff\xff', # entries[0].match.wildcards
        '\x00' * 36, # remaining match fields
        '\x00\x00\x00\x01', # entries[0].duration_sec
        '\x00\x00\x00\x02', # entries[0].duration_nsec
        '\x00\x64', # entries[0].priority
        '\x00\x05', # entries[0].idle_timeout
        '\x00\x0a', # entries[0].hard_timeout
        '\x00' * 6, # entries[0].pad2
        '\x01\x23\x45\x67\x89\xab\xcd\xef', # entries[0].cookie
        '\x00\x00\x00\x00\x00\x00\x00\x0a', # entries[0].packet_count
        '\x00\x00\x00\x00\x00\x00\x03\xe8', # entries[0].byte_count
        '\x00\x00', # entries[0].actions[0].type
        '\x00\x08', # entries[0].actions[0].len
        '\x00\x01', # entries[0].actions[0].port
        '\x00\x00', # entries[0].actions[0].max_len
        '\x00\x00', # entries[0].actions[1].type
        '\x00\x08', # entries[0].actions[1].len
        '\x00\x02', # entries[0].actions[1].port
        '\x00\x00', # entries[0].actions[1].max_len
        '\x00\x70', # entries[1].length
        '\x04', # entries[1].table_id
        '\x00', # entries[1].pad
        '\x00\x3f\xff\xff', # entries[1].match.wildcards
        '\x00' * 36, # remaining match fields
        '\x00\x00\x00\x01', # entries[1].duration_sec
        '\x00\x00\x00\x02', # entries[1].duration_nsec
        '\x00\x64', # entries[1].priority
        '\x00\x05', # entries[1].idle_timeout
        '\x00\x0a', # entries[1].hard_timeout
        '\x00' * 6, # entries[1].pad2
        '\x01\x23\x45\x67\x89\xab\xcd\xef', # entries[1].cookie
        '\x00\x00\x00\x00\x00\x00\x00\x0a', # entries[1].packet_count
        '\x00\x00\x00\x00\x00\x00\x03\xe8', # entries[1].byte_count
        '\x00\x00', # entries[1].actions[0].type
        '\x00\x08', # entries[1].actions[0].len
        '\x00\x01', # entries[1].actions[0].port
        '\x00\x00', # entries[1].actions[0].max_len
        '\x00\x00', # entries[1].actions[1].type
        '\x00\x08', # entries[1].actions[1].len
        '\x00\x02', # entries[1].actions[1].port
        '\x00\x00', # entries[1].actions[1].max_len
        '\x00\x00', # entries[1].actions[2].type
        '\x00\x08', # entries[1].actions[2].len
        '\x00\x03', # entries[1].actions[2].port
        '\x00\x00', # entries[1].actions[2].max_len
    ])

    def test_flow_stats_reply_pack(self):
        msg = ofp.message.flow_stats_reply(xid=6, flags=0, entries=[
            ofp.flow_stats_entry(table_id=3,
                                 match=ofp.match(),
                                 duration_sec=1,
                                 duration_nsec=2,
                                 priority=100,
                                 idle_timeout=5,
                                 hard_timeout=10,
                                 cookie=0x0123456789abcdef,
                                 packet_count=10,
                                 byte_count=1000,
                                 actions=[ofp.action.output(port=1),
                                          ofp.action.output(port=2)]),
            ofp.flow_stats_entry(table_id=4,
                                 match=ofp.match(),
                                 duration_sec=1,
                                 duration_nsec=2,
                                 priority=100,
                                 idle_timeout=5,
                                 hard_timeout=10,
                                 cookie=0x0123456789abcdef,
                                 packet_count=10,
                                 byte_count=1000,
                                 actions=[ofp.action.output(port=1),
                                          ofp.action.output(port=2),
                                          ofp.action.output(port=3)])])
        self.assertEquals(self.sample_flow_stats_reply_buf, msg.pack())

    def test_flow_stats_reply_unpack(self):
        msg = ofp.message.flow_stats_reply.unpack(self.sample_flow_stats_reply_buf)
        self.assertEquals(ofp.OFPST_FLOW, msg.stats_type)
        self.assertEquals(2, len(msg.entries))
        self.assertEquals(2, len(msg.entries[0].actions))
        self.assertEquals(3, len(msg.entries[1].actions))

    def test_flow_add_show(self):
        expected = """\
flow_add {
  xid = None,
  match = match_v1 {
    wildcards = OFPFW_DL_SRC|OFPFW_DL_DST,
    in_port = 3,
    eth_src = 01:23:45:67:89:ab,
    eth_dst = cd:ef:01:23:45:67,
    vlan_vid = 0x0,
    vlan_pcp = 0x0,
    eth_type = 0x0,
    ip_dscp = 0x0,
    ip_proto = 0x0,
    ipv4_src = 192.168.3.127,
    ipv4_dst = 255.255.255.255,
    tcp_src = 0x0,
    tcp_dst = 0x0
  },
  cookie = 0x0,
  idle_timeout = 0x0,
  hard_timeout = 0x0,
  priority = 0x0,
  buffer_id = 0x0,
  out_port = 0,
  flags = 0x0,
  actions = [
    output { port = OFPP_FLOOD, max_len = 0x0 },
    nicira_dec_ttl {  },
    bsn_set_tunnel_dst { dst = 0x0 }
  ]
}"""
        msg = ofp.message.flow_add(
            match=ofp.match(
                wildcards=ofp.OFPFW_DL_SRC|ofp.OFPFW_DL_DST,
                in_port=3,
                ipv4_src=0xc0a8037f,
                ipv4_dst=0xffffffff,
                eth_src=[0x01, 0x23, 0x45, 0x67, 0x89, 0xab],
                eth_dst=[0xcd, 0xef, 0x01, 0x23, 0x45, 0x67]),
            actions=[
                ofp.action.output(port=ofp.OFPP_FLOOD),
                ofp.action.nicira_dec_ttl(),
                ofp.action.bsn_set_tunnel_dst()])
        self.assertEquals(msg.show(), expected)

    sample_packet_out_buf = ''.join([
        '\x01', '\x0d', # version/type
        '\x00\x23', # length
        '\x12\x34\x56\x78', # xid
        '\xab\xcd\xef\x01', # buffer_id
        '\xff\xfe', # in_port
        '\x00\x10', # actions_len
        '\x00\x00', # actions[0].type
        '\x00\x08', # actions[0].len
        '\x00\x01', # actions[0].port
        '\x00\x00', # actions[0].max_len
        '\x00\x00', # actions[1].type
        '\x00\x08', # actions[1].len
        '\x00\x02', # actions[1].port
        '\x00\x00', # actions[1].max_len
        'abc' # data
    ])

    def test_packet_out_pack(self):
        msg = ofp.message.packet_out(
            xid=0x12345678,
            buffer_id=0xabcdef01,
            in_port=ofp.OFPP_LOCAL,
            actions=[
                ofp.action.output(port=1),
                ofp.action.output(port=2)],
            data='abc')
        self.assertEquals(self.sample_packet_out_buf, msg.pack())

    def test_packet_out_unpack(self):
        msg = ofp.message.packet_out.unpack(self.sample_packet_out_buf)
        self.assertEquals(0x12345678, msg.xid)
        self.assertEquals(0xabcdef01, msg.buffer_id)
        self.assertEquals(ofp.OFPP_LOCAL, msg.in_port)
        self.assertEquals(2, len(msg.actions))
        self.assertEquals(1, msg.actions[0].port)
        self.assertEquals(2, msg.actions[1].port)
        self.assertEquals('abc', msg.data)

    sample_packet_in_buf = ''.join([
        '\x01', '\x0a', # version/type
        '\x00\x15', # length
        '\x12\x34\x56\x78', # xid
        '\xab\xcd\xef\x01', # buffer_id
        '\x00\x09', # total_len
        '\xff\xfe', # in_port
        '\x01', # reason
        '\x00', # pad
        'abc', # data
    ])

    def test_packet_in_pack(self):
        msg = ofp.message.packet_in(
            xid=0x12345678,
            buffer_id=0xabcdef01,
            total_len=9,
            in_port=ofp.OFPP_LOCAL,
            reason=ofp.OFPR_ACTION,
            data='abc')
        self.assertEquals(self.sample_packet_in_buf, msg.pack())

    def test_packet_in_unpack(self):
        msg = ofp.message.packet_in.unpack(self.sample_packet_in_buf)
        self.assertEquals(0x12345678, msg.xid)
        self.assertEquals(0xabcdef01, msg.buffer_id)
        self.assertEquals(9, msg.total_len)
        self.assertEquals(ofp.OFPP_LOCAL, msg.in_port)
        self.assertEquals(ofp.OFPR_ACTION, msg.reason)
        self.assertEquals('abc', msg.data)

    sample_queue_get_config_reply_buf = ''.join([
        '\x01', '\x15', # version/type
        '\x00\x50', # length
        '\x12\x34\x56\x78', # xid
        '\xff\xfe', # port
        '\x00\x00\x00\x00\x00\x00', # pad
        '\x00\x00\x00\x01', # queues[0].queue_id
        '\x00\x18', # queues[0].len
        '\x00\x00', # queues[0].pad
        '\x00\x01', # queues[0].properties[0].type
        '\x00\x10', # queues[0].properties[0].length
        '\x00\x00\x00\x00', # queues[0].properties[0].pad
        '\x00\x05', # queues[0].properties[0].rate
        '\x00\x00\x00\x00\x00\x00', # queues[0].properties[0].pad2
        '\x00\x00\x00\x02', # queues[1].queue_id
        '\x00\x28', # queues[1].len
        '\x00\x00', # queues[1].pad
        '\x00\x01', # queues[1].properties[0].type
        '\x00\x10', # queues[1].properties[0].length
        '\x00\x00\x00\x00', # queues[1].properties[0].pad
        '\x00\x06', # queues[1].properties[0].rate
        '\x00\x00\x00\x00\x00\x00', # queues[1].properties[0].pad2
        '\x00\x01', # queues[1].properties[1].type
        '\x00\x10', # queues[1].properties[1].length
        '\x00\x00\x00\x00', # queues[1].properties[1].pad
        '\x00\x07', # queues[1].properties[1].rate
        '\x00\x00\x00\x00\x00\x00', # queues[1].properties[1].pad2
    ])

    def test_queue_get_config_reply_pack(self):
        msg = ofp.message.queue_get_config_reply(
            xid=0x12345678,
            port=ofp.OFPP_LOCAL,
            queues=[
                ofp.packet_queue(queue_id=1, properties=[
                    ofp.queue_prop_min_rate(rate=5)]),
                ofp.packet_queue(queue_id=2, properties=[
                    ofp.queue_prop_min_rate(rate=6),
                    ofp.queue_prop_min_rate(rate=7)])])
        self.assertEquals(self.sample_queue_get_config_reply_buf, msg.pack())

    def test_queue_get_config_reply_unpack(self):
        msg = ofp.message.queue_get_config_reply.unpack(self.sample_queue_get_config_reply_buf)
        self.assertEquals(ofp.OFPP_LOCAL, msg.port)
        self.assertEquals(msg.queues[0].queue_id, 1)
        self.assertEquals(msg.queues[0].properties[0].rate, 5)
        self.assertEquals(msg.queues[1].queue_id, 2)
        self.assertEquals(msg.queues[1].properties[0].rate, 6)
        self.assertEquals(msg.queues[1].properties[1].rate, 7)

class TestParse(unittest.TestCase):
    def test_parse_header(self):
        import loxi

        msg_ver, msg_type, msg_len, msg_xid = ofp.message.parse_header("\x01\x04\xAF\xE8\x12\x34\x56\x78")
        self.assertEquals(1, msg_ver)
        self.assertEquals(4, msg_type)
        self.assertEquals(45032, msg_len)
        self.assertEquals(0x12345678, msg_xid)

        with self.assertRaisesRegexp(loxi.ProtocolError, "too short"):
            ofp.message.parse_header("\x01\x04\xAF\xE8\x12\x34\x56")

    def test_parse_message(self):
        import loxi
        import loxi.of10 as ofp

        buf = "\x01\x00\x00\x08\x12\x34\x56\x78"
        msg = ofp.message.parse_message(buf)
        assert(msg.xid == 0x12345678)

        # Get a list of all message classes
        test_klasses = [x for x in ofp.message.__dict__.values()
                        if type(x) == type
                           and issubclass(x, ofp.message.Message)
                           and x != ofp.message.Message]

        for klass in test_klasses:
            self.assertIsInstance(ofp.message.parse_message(klass(xid=1).pack()), klass)

class TestUtils(unittest.TestCase):
    def test_pretty_wildcards(self):
        self.assertEquals("OFPFW_ALL", ofp.util.pretty_wildcards(ofp.OFPFW_ALL))
        self.assertEquals("0", ofp.util.pretty_wildcards(0))
        self.assertEquals("OFPFW_DL_SRC|OFPFW_DL_DST",
                          ofp.util.pretty_wildcards(ofp.OFPFW_DL_SRC|ofp.OFPFW_DL_DST))
        self.assertEquals("OFPFW_NW_SRC_MASK&0x2000",
                          ofp.util.pretty_wildcards(ofp.OFPFW_NW_SRC_ALL))
        self.assertEquals("OFPFW_NW_SRC_MASK&0x1a00",
                          ofp.util.pretty_wildcards(0x00001a00))
        self.assertEquals("OFPFW_IN_PORT|0x80000000",
                          ofp.util.pretty_wildcards(ofp.OFPFW_IN_PORT|0x80000000))

class TestAll(unittest.TestCase):
    """
    Round-trips every class through serialization/deserialization.
    Not a replacement for handcoded tests because it only uses the
    default member values.
    """

    def setUp(self):
        mods = [ofp.action,ofp.message,ofp.common]
        self.klasses = [klass for mod in mods
                              for klass in mod.__dict__.values()
                              if hasattr(klass, 'show')]
        self.klasses.sort(key=lambda x: str(x))

    def test_serialization(self):
        expected_failures = []
        for klass in self.klasses:
            def fn():
                obj = klass()
                if hasattr(obj, "xid"): obj.xid = 42
                buf = obj.pack()
                obj2 = klass.unpack(buf)
                self.assertEquals(obj, obj2)
            if klass in expected_failures:
                self.assertRaises(Exception, fn)
            else:
                fn()

    def test_show(self):
        expected_failures = []
        for klass in self.klasses:
            def fn():
                obj = klass()
                if hasattr(obj, "xid"): obj.xid = 42
                obj.show()
            if klass in expected_failures:
                self.assertRaises(Exception, fn)
            else:
                fn()

if __name__ == '__main__':
    unittest.main()
