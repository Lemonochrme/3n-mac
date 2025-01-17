import numpy
from gnuradio import gr
import pmt
import zlib

class mac_encode(gr.basic_block):
    def __init__(self, addr_src_size, addr_dst_size, data_size):
        gr.basic_block.__init__(
            self,
            name="mac_encode",
            in_sig=[numpy.uint8, numpy.uint8, numpy.uint8],
            out_sig=[numpy.uint8]
        )
        self.addr_src_size = addr_src_size
        self.addr_dst_size = addr_dst_size
        self.data_size = data_size
        self.set_output_multiple(addr_src_size + addr_dst_size + data_size + 4)

    def general_work(self, input_items, output_items):
        addr_src = input_items[0][:self.addr_src_size]
        addr_dst = input_items[1][:self.addr_dst_size]
        data = input_items[2][:self.data_size]

        trame = numpy.concatenate((addr_src, addr_dst, data))
        crc = zlib.crc32(trame) & 0xffffffff
        crc_bytes = numpy.array([(crc >> 24) & 0xff, (crc >> 16) & 0xff, (crc >> 8) & 0xff, crc & 0xff], dtype=numpy.uint8)
        trame_with_crc = numpy.concatenate((trame, crc_bytes))

        
        output_items[0][:len(trame_with_crc)] = trame_with_crc
        self.add_item_tag(0, self.nitems_written(0), pmt.intern("packet_len"), pmt.from_long(len(trame_with_crc)))
        self.produce(0, len(trame_with_crc))
        self.consume(0, 0)
        return len(trame_with_crc)
