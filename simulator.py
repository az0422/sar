import sys
from modules.simulator.tasks import *

version = "v3.1"

program = open(sys.argv[1], "br").read()
dmp = False

if len(sys.argv) == 3 and sys.argv[2] == "dump":
    dmp = True

memory, register, flag, time_t, clocks = run(program)

print("=================================================================")
print("SAR: Simple Architecture RICS Machine Simulator")
print("version: " + version)
print("===[RUN RESULT]==================================================")
print_runinfo([time_t, clocks])
print("---[MEMORY INFO]-------------------------------------------------")
print_memory(memory)
print("---[REGISTER INFO - SISD]----------------------------------------")
print_register_cisd(register)
print("---[REGISTER INFO - SIMD128]-------------------------------------")
print_register_simd_128b(register)
print("---[REGISTER INFO - SIMD256]-------------------------------------")
print_register_simd_256b(register)
print("-----------------------------------------------------------------")


if dmp or flag:
    open("dump", "bw").write(memory)