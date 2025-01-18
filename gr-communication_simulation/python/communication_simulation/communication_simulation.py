#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 gr-communication_simulation author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
import pmt
import zlib

class tx(gr.basic_block):
    """
    Bloc de simulation pour l'envoi de trames
    """
    def __init__(self, addr_src, addr_dst, data, addr_src_size, addr_dst_size, data_size):
        gr.basic_block.__init__(
            self,
            name="TX",
            in_sig=None,
            out_sig=[numpy.uint8, numpy.uint8, numpy.uint8]
        )
        self.addr_src = addr_src
        self.addr_dst = addr_dst
        self.data = data
        self.addr_src_size = addr_src_size
        self.addr_dst_size = addr_dst_size
        self.data_size = data_size
        # Total minimum size required per output
        self.set_output_multiple(max(self.addr_src_size, self.addr_dst_size, self.data_size))

    def general_work(self, _, output_items):
        addr_src = numpy.frombuffer(self.addr_src.encode('utf-8'), dtype=numpy.uint8)[:self.addr_src_size]
        addr_dst = numpy.frombuffer(self.addr_dst.encode('utf-8'), dtype=numpy.uint8)[:self.addr_dst_size]
        data = numpy.frombuffer(self.data.encode('utf-8'), dtype=numpy.uint8)[:self.data_size]

        output_items[0][:len(addr_src)] = addr_src
        output_items[1][:len(addr_dst)] = addr_dst
        output_items[2][:len(data)] = data

        self.add_item_tag(0, self.nitems_written(0), pmt.intern("packet_len"), pmt.from_long(len(addr_src)))
        self.add_item_tag(1, self.nitems_written(1), pmt.intern("packet_len"), pmt.from_long(len(addr_dst)))
        self.add_item_tag(2, self.nitems_written(2), pmt.intern("packet_len"), pmt.from_long(len(data)))

        self.produce(0, len(addr_src))
        self.produce(1, len(addr_dst))
        self.produce(2, len(data))
        return max(len(addr_src), len(addr_dst), len(data))

class rx(gr.basic_block):
    """
    Bloc de simulation pour la réception de trames
    """
    def __init__(self, addr_src_size, addr_dst_size, data_size):
        gr.basic_block.__init__(
            self,
            name="RX",
            in_sig=[numpy.uint8, numpy.uint8, numpy.uint8],
            out_sig=None  # No direct output signal
        )
        self.addr_src_size = addr_src_size
        self.addr_dst_size = addr_dst_size
        self.data_size = data_size
        self.message_port_register_out(pmt.intern("msg_out"))  # Register message output port

    def general_work(self, input_items, _):
        addr_src = input_items[0][:self.addr_src_size]
        addr_dst = input_items[1][:self.addr_dst_size]
        data = input_items[2][:self.data_size]

        # print(f"Source Address: {addr_src}")
        # print(f"Destination Address: {addr_dst}")
        # print(f"Data: {data}")

        msg = pmt.cons(pmt.PMT_NIL, pmt.intern(f'Source Address: {addr_src.tobytes().decode("utf-8")}, Destination Address: {addr_dst.tobytes().decode("utf-8")}, Data: {data.tobytes().decode("utf-8")}'))
        self.message_port_pub(pmt.intern("msg_out"), msg)  # Publish message

        self.consume(0, len(addr_src))
        self.consume(1, len(addr_dst))
        self.consume(2, len(data))
        return max(len(addr_src), len(addr_dst), len(data))
