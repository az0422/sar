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
                (op, tail), (ra, rb, rc, rx, ry, rz, const) = opcodes[p["opcode"]]
                rA, rB, rC = p["ra"], p["rb"], p["rc"]
                rX, rY, rZ = p["rx"], p["ry"], p["rz"]

                n[0] = op
                n[1] = registers[rA[1:]] if ra and rA is not None else 0xFF if ra else 0x00
                n[2] = registers[rB[1:]] if rb and rB is not None else 0xFF if rb else 0x00
                n[3] = registers[rC[1:]] if rc and rC is not None else 0xFF if rc else 0x00
                n[4] = registers[rX[1:]] if rx and rX is not None else 0xFF if rx else 0x00
                n[5] = registers[rY[1:]] if ry and rY is not None else 0xFF if ry else 0x00
                n[6] = registers[rZ[1:]] if rz and rZ is not None else 0xFF if rz else 0x00

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



    