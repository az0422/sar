import sys

from modules.assembler.tasks import run

filename = sys.argv[1]
assembly = open(filename, "r").read()

bytecode = run(assembly)

open(filename.split(".")[0] + ".bin", "bw").write(bytecode)