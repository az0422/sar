from modules.utils.decoder import arr2const, const2arr

def fetch(memory, pc):
    op = memory[pc]
    rA = memory[pc+1]
    rB = memory[pc+2]
    rC = memory[pc+3]
    const = arr2const(memory[pc+3:pc+7])
    tail = memory[pc+7]

    rX = memory[pc+4]
    rY = memory[pc+5]
    rZ = memory[pc+6]

    return {"op": op, "rA": rA, "rB": rB, "rC": rC, "rX": rX, "rY": rY, "rZ": rZ, "const": const, "tail": tail}

def decoder_t(in_dict):
    tail = in_dict["tail"]
    op = in_dict["op"]
    simd = 0 # 0: normal, 1: 64x2
    status = 0

    if tail >> 4 in (0xF, 0x0):
        simd = 0
    elif tail >> 4 in (0x1, 0x2):
        simd = tail >> 4
    else:
        status = 1
    
    if op == 0x00:
        status = 1
    
    in_dict["simd"] = simd
    in_dict["status"] = status

    return in_dict

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
    register_index = in_dict["simd"]

    destE = in_dict["destE"]
    destM = in_dict["destM"]

    flag = in_dict["flag"]
    all_flag = in_dict["all_flag"]

    register[0][destM] = m

    if not all_flag:
        return
    
    if register_index == 0:
        if destE == 0xFF:
            pass
        elif flag:
            register[0][destE] = e
    elif register_index in (1, 2):
        if destE[0] == 0:
            register[register_index][destE[1]] = e
        elif destE[0] == 1:
            register_addr = [destE[1] & 0x7F, destE[1] & 0x3F][register_index - 1]
            register_segm = [destE[1] >> 7, destE[1] >> 6][register_index - 1]
            register[register_index][register_addr][register_segm] = e[0]
        elif destE[0] == 2:
            for i, de in enumerate(destE[1:]):
                register[0][de] = e[i]

