import re
import sys

from .utils.opcodes import opcodes, registers
from .utils.parsor import parsor, label_count
from modules.utils.decoder import const2arr

def run(asm):
    result = bytearray()
    parse = parsor(asm)
    labels = label_count(parse)

    for p in parse:
        n = bytearray(8)

        if p["opcode"] is None:
            continue

        if p["opcode"] == ".space":
            n = bytearray(eval(p["const"][1:]))
        elif p["opcode"] == ".data":
            n = const2arr(labels[p["const"]] if p["const"] in labels.keys() else eval(p["const"][1:]))
        else:
            try:
                (op, tail), (ra, rb, rc, const) = opcodes[p["opcode"]]
                rA, rB, rC = p["ra"], p["rb"], p["rc"]

                n[0] = op
                n[1] = registers[p["ra"][1:]] if ra and rA is not None else 0xFF
                n[2] = registers[p["rb"][1:]] if rb and rB is not None else 0xFF
                n[3] = registers[p["rc"][1:]] if rc and rC is not None else 0xFF

                if const:
                    if p["const"] in labels.keys():
                        n[3:7] = const2arr(labels[p["const"]], 4)
                    elif p["const"] is not None:
                        n[3:7] = const2arr(eval(p["const"][1:]), 4)
                    else:
                        n[3:7] = const2arr(0, 4)
                
                n[7] = tail
            except:
                print("line %d\n%s\nSyntaxError: invalid syntax" % (p["index"], p["original"]))
                sys.exit()
        
        result.extend(n)
    
    return result



    