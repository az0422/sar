import sys
from modules.simulator.tasks import *

program = open(sys.argv[1], "br").read()
dmp = False

if len(sys.argv) == 3 and sys.argv[2] == "dump":
    dmp = True

memory, register = run(program)

print("===[RUN RESULT]==========================================")
print("---[MEMORY INFO]-----------------------------------------")
print_memory(memory)
print("---[REGISTER INFO]---------------------------------------")
print_register(register)
print("---------------------------------------------------------")

if dmp:
    open("dump", "bw").write(memory)