import numpy
from gnuradio import gr
import pmt
import zlib

class encode(gr.basic_block):
    def __init__(self, addr_src_size, addr_dst_size, data_size):
        gr.basic_block.__init__(
            self,
            name="encode",
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
        # self.consume(0, self.addr_src_size) Si laissé, le message debug renvoie pas toute la trame
        # self.consume(1, self.addr_dst_size)
        # self.consume(2, self.data_size)
        return len(trame_with_crc)
    

class decode(gr.basic_block):
    def __init__(self, addr_src_size, addr_dst_size, data_size):
        gr.basic_block.__init__(
            self,
            name="decode",
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8, numpy.uint8, numpy.uint8]
        )
        self.addr_src_size = addr_src_size
        self.addr_dst_size = addr_dst_size
        self.data_size = data_size
        self.set_output_multiple(max(self.addr_src_size, self.addr_dst_size, self.data_size))
    
    def general_work(self, input_items, output_items):  # Attention on lit constamment meme s'il n'y a rien
        trame_with_crc = input_items[0][:self.addr_src_size + self.addr_dst_size + self.data_size + 4] # Avec ça ça marche du feu de dieu mais pas fan
        # print(f"Decode - Received Trame: {trame_with_crc}")
        trame = trame_with_crc[:-4]
        crc_received = int.from_bytes(trame_with_crc[-4:], byteorder='big')
        crc_calculated = zlib.crc32(trame) & 0xffffffff

        if crc_received != crc_calculated:
            raise ValueError("CRC mismatch")

        addr_src = trame[:self.addr_src_size]
        addr_dst = trame[self.addr_src_size:self.addr_src_size + self.addr_dst_size]
        data = trame[self.addr_src_size + self.addr_dst_size:self.addr_src_size + self.addr_dst_size + self.data_size]

        output_items[0][:len(addr_src)] = addr_src
        output_items[1][:len(addr_dst)] = addr_dst
        output_items[2][:len(data)] = data
        self.add_item_tag(0, self.nitems_written(0), pmt.intern("packet_len"), pmt.from_long(len(addr_src)))
        self.add_item_tag(1, self.nitems_written(1), pmt.intern("packet_len"), pmt.from_long(len(addr_dst)))
        self.add_item_tag(2, self.nitems_written(2), pmt.intern("packet_len"), pmt.from_long(len(data)))
        self.produce(0, len(addr_src))
        self.produce(1, len(addr_dst))
        self.produce(2, len(data))
        self.consume(0, len(trame_with_crc))
        return max(len(addr_src), len(addr_dst), len(data))
