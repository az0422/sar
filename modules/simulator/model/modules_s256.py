def decoder_a(in_dict, register):
    rA = in_dict["rA"]
    rB = in_dict["rB"]
    rC = in_dict["rC"]
    rX = in_dict["rX"]
    rY = in_dict["rY"]
    simd = in_dict["simd"]

    data_a = register[2][rA & 0x3F]
    data_b = register[2][rB & 0x3F]
    data_c = register[2][rC & 0x3F]
    data_x = register[2][rX & 0x3F]

    op = in_dict["op"]
    tail = in_dict["tail"]
    status = 0 # 0: AOK, 1: halt, 2: nop

    if tail == 0x20:
        if op == 0x41: # rcopyss256
            data_b = [0, 0, 0, 0]
        elif op == 0x42: # rcopyns256
            t = register[0][rA]
            data_a = [t, 0, 0, 0]
            data_b = [0, 0, 0, 0]
        elif op == 0x43: # rcopysn256
            data_a = data_a[rA >> 6]
            data_b = 0
            simd = 0
        elif op == 0x44: # rcopyns256all
            t = register[0][rA]
            data_a = [t, t, t, t]
            data_b = [0, 0, 0, 0]
        elif op in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57):
            pass
        else:
            status = 1

    elif tail == 0x21:
        if op == 0x42: # rcopyns256q
            data_a = [register[0][rA], register[0][rB], register[0][rC], register[0][rX]]
            data_b = [0, 0, 0, 0]
        elif op == 0x43: # rcopysn256q
            data_b = [0, 0, 0, 0]
        else:
            status = 1
    else:
        status = 1
    
    return {"data_a": data_a, "data_b": data_b, "status": status, "simd": simd, "data_s": 0, "data_c": 0,
            "rA": rA, "rB": rB, "rC": rC, "rX": rX, "rY": rY, "op": op, "tail": tail}

def decoder_b(in_dict):
    rA = in_dict["rA"]
    rB = in_dict["rB"]
    rC = in_dict["rC"]
    rX = in_dict["rX"]
    rY = in_dict["rY"]
    op = in_dict["op"]

    tail = in_dict["tail"]

    destE = 0xFF
    destM = 0xFF

    mem = 0 # 0: pass, 1: read, 2: write, 3: pop, 4: push
    alu = 0x0 # 0: add, 1: sub, 2: shr, 3: shl, 4: and, 5: or, 6: not, 7: xor

    cc = 0x7
    cc_u = 0

    if tail == 0x20:
        if op  >> 4 == 0x4:
            destE = [0, rB & 0x3F]
            if op == 0x42:
                destE = [1, rB]
        elif op >> 4 == 0x5:
            alu = op & 0xF
            destE = [0, rC & 0x3F]
    
    elif tail == 0x21:
        if op == 0x42:
            destE = [0, rY & 0x3F]
        elif op == 0x43:
            destE = [2, rB, rC, rX, rY]
    
    return {"data_a": in_dict["data_a"], "data_b": in_dict["data_b"], "simd": in_dict["simd"], "data_c": 0, "data_s": 0,
            "destE": destE, "destM": destM, "alu": alu, "mem": mem, "cc": cc, "cc_u": cc_u}