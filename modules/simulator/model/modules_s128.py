def decoder_a(in_dict, register):
    data_a = register[1][in_dict["rA"] & 0x7F]
    data_b = register[1][in_dict["rB"] & 0x7F]
    
    rA = in_dict["rA"]
    rB = in_dict["rB"]
    rC = in_dict["rC"]

    simd = in_dict["simd"]

    op = in_dict["op"]
    tail = in_dict["tail"]
    status = 0 # 0: AOK, 1: halt, 2: nop

    if tail == 0x10:
        if op == 0x41: # rcopyss
            data_b = [0, 0]
        elif op == 0x42: # rcopyns
            t = register[0][rA]
            data_a = [t, 0]
            data_b = [0, 0]
        elif op == 0x43: # rcopysn
            data_a = data_a[rA >> 7]
            data_b = 0
            simd = 0
        elif op == 0x44: # rcopynsall
            t = register[0][rA]
            data_a = [t, t]
            data_b = [0, 0]
        elif op in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57):
            pass
        else:
            status = 1
    else:
        status = 1
    
    return {"data_a": data_a, "data_b": data_b, "status": status, "simd": simd, "data_s": 0, "data_c": 0,
            "rA": rA, "rB": rB, "rC": rC, "op": op, "tail": tail}

def decoder_b(in_dict):
    rA = in_dict["rA"]
    rB = in_dict["rB"]
    rC = in_dict["rC"]
    op = in_dict["op"]

    tail = in_dict["tail"]

    destE = 0xFF
    destM = 0xFF

    mem = 0 # 0: pass, 1: read, 2: write, 3: pop, 4: push
    alu = 0x0 # 0: add, 1: sub, 2: shr, 3: shl, 4: and, 5: or, 6: not, 7: xor

    cc = 0x7
    cc_u = 0

    if tail == 0x10:
        if op  >> 4 == 0x4:
            destE = [0, rB & 0x3F]
            if op == 0x42:
                destE = [1, rB]
        elif op >> 4 == 0x5:
            alu = op & 0xF
            destE = [0, rC & 0x3F]
    
    return {"data_a": in_dict["data_a"], "data_b": in_dict["data_b"], "simd": in_dict["simd"], "data_c": 0, "data_s": 0,
            "destE": destE, "destM": destM, "alu": alu, "mem": mem, "cc": cc, "cc_u": cc_u}


def alu(in_dict):
    alu = in_dict["alu"]
    
    a = in_dict["data_a"]
    b = in_dict["data_b"]
    e = []
    lim = 0xFFFFFFFFFFFFFFFF

    if alu == 0:
        e = [(aa + bb) & lim for aa, bb in zip(a, b)]
    
    elif alu == 1:
        e = [(aa - bb) & lim for aa, bb in zip(a, b)]
    
    elif alu == 2:
        e = [(aa >> bb) & lim for aa, bb in zip(a, b)]
    
    elif alu == 3:
        e = [(aa << bb) & lim for aa, bb in zip(a, b)]
    
    elif alu == 4:
        e = [(aa & bb) & lim for aa, bb in zip(a, b)]

    elif alu == 5:
        e = [(aa | bb) & lim for aa, bb in zip(a, b)]
    
    elif alu == 6:
        e = [(~aa) & lim for aa, bb in zip(a, b)]
    
    elif alu == 7:
        e = [(aa ^ bb) & lim for aa, bb in zip(a, b)]

    return {"destE": in_dict["destE"], "destM": in_dict["destM"], "mem": in_dict["mem"], "data_s": 0, "data_c": 0,
        "cc": 7, "data_e": e}