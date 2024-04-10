from .modules import *

class Model:
    def __init__(self, program):
        self.memory = bytearray(program)
        self.register = [0 for _ in range(0x100 + 1)]
        self.register[0xFF] = 0
        self.cc = 7
        self.status = 0
    
    def run(self):
        if self.status == 1:
            return

        fetch_dict = fetch(self.memory, self.register[0x100])
        self.register[0x100] += 8

        decoder_a_dict = decoder_a(fetch_dict, self.register)

        self.status |= decoder_a_dict["status"]

        decoder_b_dict = decoder_b(decoder_a_dict)

        alu_dict = alu(decoder_b_dict)

        cc_u = decoder_b_dict["cc_u"]

        if cc_u:
            self.cc = alu_dict["cc"]
        
        memory_dict = memory(alu_dict, self.memory)

        wb_in = {"data_e": memory_dict["data_e"], "data_m": memory_dict["data_m"], "destE": decoder_b_dict["destE"],
                 "destM": decoder_b_dict["destM"], "flag": self.cc & decoder_b_dict["cc"]}

        writeback(wb_in, self.register)

        self.register[0xFF] = 0

        #return fetch_dict, decoder_a_dict, decoder_b_dict, alu_dict, memory_dict, self.cc
        return None

