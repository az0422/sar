from .modules import *
from . import modules_64 as s64, modules_s128 as s128

class Model:
    def __init__(self, program):
        self.memory = bytearray(program)
        self.register = [[0 for _ in range(0x100 + 1)],
                         [[0, 0] for _ in range(0x80)],
                        ]
        self.register[0][0xFF] = 0
        self.cc = 7
        self.status = 0
    
    def run(self):
        # pipe 0
        fetch_dict = fetch(self.memory, self.register[0][0x100])
        self.register[0][0x100] += 8

        # pipe 1
        decoder_t_dict = decoder_t(fetch_dict)
        
        self.status |= decoder_t_dict["status"]

        simd = decoder_t_dict["simd"]
        if simd:
            decoder_a = s128.decoder_a
        else:
            decoder_a = s64.decoder_a

        # pipe 2
        decoder_a_dict = decoder_a(fetch_dict, self.register)

        self.status |= decoder_a_dict["status"]

        simd = decoder_a_dict["simd"]
        if simd:
            decoder_b = s128.decoder_b
            alu = s128.alu
        else:
            decoder_b = s64.decoder_b
            alu = s64.alu

        # pipe 3
        decoder_b_dict = decoder_b(decoder_a_dict)

        # pipe 4
        alu_dict = alu(decoder_b_dict)

        cc_u = decoder_b_dict["cc_u"]

        if cc_u:
            self.cc = alu_dict["cc"]
        
        # pipe 5
        memory_dict = memory(alu_dict, self.memory)

        # pipe 6
        wb_in = {"data_e": memory_dict["data_e"], "data_m": memory_dict["data_m"], "destE": decoder_b_dict["destE"],
                 "destM": decoder_b_dict["destM"], "flag": self.cc & decoder_b_dict["cc"], "simd": simd}

        writeback(wb_in, self.register)

        self.register[0][0xFF] = 0

        #return fetch_dict, decoder_a_dict, decoder_b_dict, alu_dict, memory_dict, self.cc
        return None

