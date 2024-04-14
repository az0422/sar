from .model.model import Model
from time import time

def run(program):
    machine = Model(program)
    
    clocks = 1
    end_t = 0
    try:
        start_t = time()
        while not machine.status:
            t = machine.run()
            if t: print(t)

            clocks += 1

        end_t = time() - start_t
    except KeyboardInterrupt:
        return machine.memory, machine.register, True, 0, clocks
    
    return machine.memory, machine.register, False, end_t, clocks

def print_memory(memory):
    for i, b in enumerate(memory):
        print("%02X" % b, end=" ")

        if (i + 1) % 0x10 == 0:
            print()
    print()

def print_register_cisd(register):
    register_name = ["main", "cycl", "data", "addr", "args", "func", "iovr", "sysm"]

    for i, b in enumerate(register[0][:-3]):
        print("%s%x %02X %016X" % (register_name[i // 32], i % 32, i, b))
    print("stck FE %016X" % register[0][-3])
    print("null FF %016X" % 0)
    print("PC      %016X" % register[0][-1])

def print_register_simd_64b(register):
    register_name = "s128b"
    
    for i, b in enumerate(register[1]):
        print("%s%x %02X h(%02X):%016X l(%02X):%016X" % (register_name, i, i, i, b[0], i | 0x80, b[1]))

def print_runinfo(info):
    print("Run time:", info[0], "s")
    print("Clocks:", info[1], "cycle" + ("s" if info[1] > 1 else ""))