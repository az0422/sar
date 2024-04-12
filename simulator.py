import sys
from modules.simulator.tasks import *

version = "v1.2"

program = open(sys.argv[1], "br").read()
dmp = False

if len(sys.argv) == 3 and sys.argv[2] == "dump":
    dmp = True

memory, register, flag, time_t, clocks = run(program)

print("=========================================================")
print("SAR: Simple Architecture RICS Machine Simulator")
print("version: " + version)
print("===[RUN RESULT]==========================================")
print_runinfo([time_t, clocks])
print("---[MEMORY INFO]-----------------------------------------")
print_memory(memory)
print("---[REGISTER INFO]---------------------------------------")
print_register(register)
print("---------------------------------------------------------")

if dmp or flag:
    open("dump", "bw").write(memory)