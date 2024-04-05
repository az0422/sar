from .modules import *

class Model:
    def __init__(self, program):
        self.memory = bytearray(program)
        self.register = [0 for _ in range(0x100 + 1)]
        self.register[0xFF] = 0
        self.cc = 7
        self.status = 0
    
    def run(self):
        if self.status:
            return

        f = fetch(self.memory, self.register[0x100])
        self.register[0x100] += 8

        d = decoder(f, self.register)

        self.status |= d["status"]

        a = alu(d)

        cc_u = d["cc_u"]

        if cc_u:
            self.cc = a["cc"]
        
        m_in = {"mem": d["mem"], "e": a["e"], "data_c": d["data_c"]}
        m = memory(m_in, self.memory)

        wb_in = {"e": a["e"], "m": m["m"], "destE": d["destE"], "destM": d["destM"], "flag": self.cc & d["cc"]}

        writeback(wb_in, self.register)

        self.register[0xFF] = 0

