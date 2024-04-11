import re

from .opcodes import opcodes, registers

def parsor(asm):
    result = []

    for i, record in enumerate(asm.split("\n")):
        record_s = record.strip()
        r = re.search("(?P<label>[0-9a-zA-Z._]+:)?"
                    + "(\s+)?((?P<opcode>[.a-z0-9]+)"
                    + "(\s+(?P<ra>%[a-z0-9]+)(\s*,\s*(?P<rb>%[a-z0-9]+)(\s*,\s*(?P<rc>%[a-z0-9]+))?)?)?"
                    + "(\s*(,\s*)?(?P<const>\$[0-9a-zA-Z._]+))?)?"
                    + "(?P<comment>#.*)?", record_s).groupdict()
        
        r["index"] = i + 1
        r["original"] = record

        result.append(r)
    
    return trim(result)

def trim(parse):
    for p in parse:
        opcode = p["opcode"]
        if opcode is None:
            continue
        ra = p["ra"]

        if (not opcodes[opcode][1][0]) and (opcodes[opcode][1][1]):
            p["ra"] = None
            p["rb"] = ra
    
    return parse

def label_count(record):
    labels = {}
    pc = 0

    for r in record:
        if r["label"]  is not None:
            labels["$" + r["label"][:-1]] = pc
        
        if r["opcode"] == ".space":
            pc += eval(r["const"][1:])

        if r["opcode"] is not None:
            pc += 8
    
    return labels