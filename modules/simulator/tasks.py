from .model.model import Model

def run(program):
    machine = Model(program)
    
    try:
        while not machine.status:
            t = machine.run()
            if t: print(t)
    except KeyboardInterrupt:
        return machine.memory, machine.register, True
    
    return machine.memory, machine.register, False

def print_memory(memory):
    for i, b in enumerate(memory):
        print("%02X" % b, end=" ")

        if (i + 1) % 0x10 == 0:
            print()
    print()

def print_register(register):
    register_name = ["main", "cycl", "data", "addr", "args", "func", "iovr", "sysm"]

    for i, b in enumerate(register[:-3]):
        print("%s%x %02X %016X" % (register_name[i // 32], i % 32, i, b))
    print("stck FE %016X" % register[-3])
    print("null FF %016X" % 0)
    print("PC      %016X" % register[-1])
