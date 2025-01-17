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

class communication_simulation(gr.basic_block):
    """
    Bloc de simulation pour l'envoi de trames
    """
    def __init__(self, addr_src, addr_dst, data, addr_src_size, addr_dst_size, data_size):
        gr.basic_block.__init__(
            self,
            name="communication_simulation",
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
        addr_src_bytes = numpy.frombuffer(self.addr_src.encode('utf-8'), dtype=numpy.uint8)[:self.addr_src_size]
        addr_dst_bytes = numpy.frombuffer(self.addr_dst.encode('utf-8'), dtype=numpy.uint8)[:self.addr_dst_size]
        data_bytes = numpy.frombuffer(self.data.encode('utf-8'), dtype=numpy.uint8)[:self.data_size]

        addr_src_len = len(addr_src_bytes)
        addr_dst_len = len(addr_dst_bytes)
        data_len = len(data_bytes)


        output_items[0][:addr_src_len] = addr_src_bytes
        output_items[1][:addr_dst_len] = addr_dst_bytes
        output_items[2][:data_len] = data_bytes

        self.add_item_tag(0, self.nitems_written(0), pmt.intern("packet_len"), pmt.from_long(addr_src_len))
        self.add_item_tag(1, self.nitems_written(1), pmt.intern("packet_len"), pmt.from_long(addr_dst_len))
        self.add_item_tag(2, self.nitems_written(2), pmt.intern("packet_len"), pmt.from_long(data_len))

        self.produce(0, addr_src_len)
        self.produce(1, addr_dst_len)
        self.produce(2, data_len)
        self.consume(0, 0)
        return max(addr_src_len, addr_dst_len, data_len)

