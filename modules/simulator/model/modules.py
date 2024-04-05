from modules.utils.decoder import arr2const, const2arr

def fetch(memory, pc):
    op = memory[pc]
    rA = memory[pc+1]
    rB = memory[pc+2]
    const = arr2const(memory[pc+3:pc+7])

    return {"op": op, "rA": rA, "rB": rB, "const": const}


def decoder(in_dict, register):
    alu = 0 # 0: add, 1: sub, 2: shr, 3: shl, 4: and, 5: or, 6: not, 7: xor
    mem = 0 # 0: pass, 1: read, 2: write, 3: pop
    status = 0 # 0: AOK, 1: halt
    destE = 0xFF
    destM = 0xFF
    cc = 0x7
    cc_u = 0

    data_a = register[in_dict["rA"]]
    data_b = register[in_dict["rB"]]
    data_c = in_dict["const"]
    op = in_dict["op"]

    if op == 0x00: # halt
        status = 1

    elif op == 0x10: # nop
        pass

    elif op >> 4 == 0x2: # mread, pop
        mem = 1
        destM = in_dict["rB"]

        if op & 0x0F:
            data_a = register[0xFE]
            data_b = 8
            destE = 0xFE
            alu = 0
    
    elif op >> 4 == 0x3: # mwrite, push
        mem = 2
        data_c = data_a

        if op & 0x0F:
            data_a = register[0xFE]
            data_b = 8
            destE = 0xFE
            alu = 1
    
    elif op >> 4 == 0x4: # iread
        data_a = data_c
        data_b = 0
        destE = in_dict["rB"]
    
    elif op >> 4 == 0x5: # add, sub, shr, shl, and, or, not, xor
        alu = op & 0x0F
        cc_u = 1
        destE = in_dict["rB"]
    
    elif op >> 4 == 0x6: # jump, jl, jle, je, jge, jg, jne
        cc = [7, 1, 5, 4, 6, 2, 3][op & 0x0F]
        destE = 0x100
    
    elif op >> 4 == 0x7: # call, ret
        call_position = data_c
        data_a = register[0xFE]
        data_b = 8
        data_c = register[0x100]
        alu = 1
        mem = 2
        destE = 0xFE

        if op & 0xF:
            alu = 0
            mem = 3
            destM = 0x100
            destE = 0xFE
        else:
            register[0x100] = call_position
            
    else:
        status = 1
    
    return {"data_a": data_a, "data_b": data_b, "data_c": data_c, "alu": alu, "mem": mem, "status": status,
            "destE": destE, "destM": destM, "cc": cc, "cc_u": cc_u}

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

    return {"cc": eql << 3 | grt << 2 | les, "e": e}

def memory(in_dict, memory):
    mem = in_dict["mem"]
    e = in_dict["e"]

    if mem == 0:
        return {"m": 0}
    if mem == 1:
        return {"m": arr2const(memory[e:e+8])}
    if mem == 2:
        memory[e:e+8] = const2arr(in_dict["data_c"])
        return {"m": 0}
    if mem == 3:
        return {"m": arr2const(memory[e-8:e])}
    
def writeback(in_dict, register):
    e = in_dict["e"]
    m = in_dict["m"]

    destE = in_dict["destE"]
    destM = in_dict["destM"]

    flag = in_dict["flag"]

    register[destM] = m

    if flag: register[destE] = e

