from modules.utils.decoder import arr2const, const2arr

def fetch(memory, pc):
    op = memory[pc]
    rA = memory[pc+1]
    rB = memory[pc+2]
    rC = memory[pc+3]
    const = arr2const(memory[pc+3:pc+7])
    tail = memory[pc+7]

    return {"op": op, "rA": rA, "rB": rB, "rC": rC, "const": const, "tail": tail}

def decoder_a(in_dict, register):
    data_a = register[in_dict["rA"]]
    data_b = register[in_dict["rB"]]
    data_c = in_dict["const"]
    data_s = register[0xFE]
    op = in_dict["op"]
    tail = in_dict["tail"]
    status = 0 # 0: AOK, 1: halt, 2: nop

    if tail in (0x00, 0xFF):
        if op == 0x00: # halt
            status = 1
            data_a = 0
            data_b = 0
        elif op == 0x10: # nop
            status = 2
            data_a = 0
            data_b = 0
        elif op == 0x20: # mread
            data_b = data_c
        elif op == 0x21: # pop
            pass
        elif op == 0x30: # mwrite
            t = data_a
            data_a = data_b
            data_b = data_c
            data_c = t
        elif op == 0x31: # push
            pass
        elif op == 0x40: # iread
            data_a = data_c
            data_b = 0
        elif op == 0x41:
            data_b = 0
            data_c = 0
        elif op in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58): # op
            pass
        elif op in (0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66): # jumps
            data_a = data_b
            data_b = data_c
        elif op == 0x70: # call
            t = register[0x100]
            register[0x100] = data_c + data_b
            data_c = t
        elif op == 0x71: # ret
            pass
        else:
            status = 1
    
    elif tail == 0x01:
        if op in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57):
            pass
        else: status = 1
    
    elif tail == 0x02:
        if op == 0x58:
            t = data_a
            data_a = data_c
            data_b = t
        else:
            status = 1
    else:
        status = 1
    
    return {"data_a": data_a, "data_b": data_b, "data_c": data_c, "data_s": data_s, "status": status,
            "rA": in_dict["rA"], "rB": in_dict["rB"], "rC": in_dict["rC"], "op": op, "tail": tail}

def decoder_b(in_dict):
    rA = in_dict["rA"]
    rB = in_dict["rB"]
    rC = in_dict["rC"]
    op = in_dict["op"]

    tail = in_dict["tail"]

    destE = 0xFF
    destM = 0xFF

    mem = 0 # 0: pass, 1: read, 2: write, 3: pop, 4: push
    alu = 0 # 0: add, 1: sub, 2: shr, 3: shl, 4: and, 5: or, 6: not, 7: xor

    cc = 0x7
    cc_u = 0
    
    if tail in (0x00, 0xFF):
        if op == 0x00: # halt
            pass
        elif op == 0x10: # nop
            pass
        elif op == 0x20: # mread
            mem = 1
            destM = rB
        elif op == 0x21: # pop
            mem = 3
            destM = rB
            destE = 0xFE
        elif op == 0x30: # mwrite
            mem = 2
        elif op == 0x31: # push
            mem = 4
            destE = 0xFE
        elif op == 0x40: # iread
            destE = rB
        elif op == 0x41: # rcopy
            destE = rB
        elif op >> 4 == 0x5: # op
            destE = rB
            alu = op & 0x7
            cc_u = 1

            if op == 0x58:
                destE = 0xFF
                alu = 1

        elif op >> 4 == 0x6: # jumps
            destE = 0x100
            cc = [7, 1, 5, 4, 6, 2, 3][op & 0x0F]
        elif op == 0x70: # call
            destE = 0xFE
            mem = 4
        elif op == 0x71: # ret
            mem = 3
            destM = 0x100
            destE = 0xFE

    elif tail == 0x01:
        if op >> 4 == 0x5:
            destE = rC
            alu = op & 0x7
            cc_u = 1
    
    elif tail == 0x02:
        if op == 0x58:
            destE = 0xFF
            alu = 1
            cc_u = 1
    
    return {"data_a": in_dict["data_a"], "data_b": in_dict["data_b"], "data_c": in_dict["data_c"], "data_s": in_dict["data_s"],
            "destE": destE, "destM": destM, "alu": alu, "mem": mem, "cc": cc, "cc_u": cc_u}


def alu(in_dict):
    alu = in_dict["alu"]
    
    a = in_dict["data_a"]
    b = in_dict["data_b"]
    e = 0x00
    
    les = 0
    eql = 0
    grt = 0

    if alu == 0:
        e = a + b
    
    elif alu == 1:
        e = a - b
    
    elif alu == 2:
        e = a >> b
    
    elif alu == 3:
        e = a << b
    
    elif alu == 4:
        e = a & b

    elif alu == 5:
        e = a | b
    
    elif alu == 6:
        e = ~a
    
    elif alu == 7:
        e = a ^ b
    
    # limit 64bit
    e = e & 0xFFFFFFFFFFFFFFFF
    
    # get MSB from operand
    aSF = a >> 63 & 0x1
    bSF = b >> 63 & 0x1
    
    # set flags
    ZF = int(e == 0x00)
    SF = e >> 63
    OF = (~aSF & ~bSF & SF) | (aSF & bSF & ~SF) if alu == 0 else 0
    
    # set CC flag
    eql = ZF
    les = SF ^ OF
    grt = ~ZF & ~(SF ^ OF) & 0x1 

    return {"destE": in_dict["destE"], "destM": in_dict["destM"], "data_c": in_dict["data_c"], "data_s": in_dict["data_s"], "mem": in_dict["mem"],
        "cc": eql << 2 | grt << 1 | les, "data_e": e}

def memory(in_dict, memory):
    mem = in_dict["mem"]
    e = in_dict["data_e"]
    data_s = in_dict["data_s"]
    data_c = in_dict["data_c"]

    if mem == 0: # pass
        return {"data_m": 0, "data_e": e}
    if mem == 1: # read
        return {"data_m": arr2const(memory[e:e+8]), "data_e": e}
    if mem == 2: # write
        memory[e:e+8] = const2arr(data_c)
        return {"data_m": 0, "data_e": e}
    if mem == 3: # pop
        e = data_s + 8
        return {"data_m": arr2const(memory[e-8:e]), "data_e": e}
    if mem == 4: # push
        e = data_s - 8
        memory[e:e+8] = const2arr(data_c)
        return {"data_m": 0, "data_e": e}

    
def writeback(in_dict, register):
    e = in_dict["data_e"]
    m = in_dict["data_m"]

    destE = in_dict["destE"]
    destM = in_dict["destM"]

    flag = in_dict["flag"]

    register[destM] = m

    if flag: register[destE] = e

