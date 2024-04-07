import re

from .opcodes import opcodes, registers

opcodes_str = "|".join([s for s in opcodes.keys()])
registers_str = "|".join([s for s in registers.keys()])

def parsor(asm):
    result = []

    for i, record in enumerate(asm.split("\n")):
        record_s = record.strip()
        r = re.search("(?P<label>[0-9a-zA-Z._]+:)?"
                    + "(\s+)?((?P<opcode>(" + opcodes_str + "))"
                    + "(\s+(?P<ra>%(" + registers_str + "))(\s*,\s*(?P<rb>%(" + registers_str + ")))?)?"
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