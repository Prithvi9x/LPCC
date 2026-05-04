optab = {
    "STOP": ("IS", 0),
    "ADD": ("IS", 1),
    "SUB": ("IS", 2),
    "MULT": ("IS", 3),
    "MOVER": ("IS", 4),
    "MOVEM": ("IS", 5),
    "COMP": ("IS", 6),
    "BC": ("IS", 7),
    "DIV": ("IS", 8),
    "READ": ("IS", 9),
    "PRINT": ("IS", 10),
    "START": ("AD", 1),
    "END": ("AD", 2),
    "LTORG": ("AD", 3),
    "DS": ("DL", 1),
    "DC": ("DL", 2),
}

registers = {
    "AREG": 1,
    "BREG": 2,
    "CREG": 3,
    "DREG": 4
}

def generate_ic(lines):
    ic = []
    lc = 0

    for line in lines:
        parts = line.split()
        if not parts:
            continue

        if parts[0] == "START":
            lc = int(parts[1])
            ic.append(f"(AD,1) (C,{lc})")
            continue

        if len(parts) == 3:
            _, opcode, operand = parts
        elif len(parts) == 2:
            opcode, operand = parts
        else:
            opcode = parts[0]
            operand = None

        if opcode in optab:
            code = optab[opcode]

            if operand:
                if operand in registers:
                    ic.append(f"(IS,{code[1]}) (R,{registers[operand]})")
                elif operand.isdigit():
                    ic.append(f"(IS,{code[1]}) (C,{operand})")
                else:
                    ic.append(f"(IS,{code[1]}) (S,{operand})")
            else:
                ic.append(f"(IS,{code[1]})")

        lc += 1

    return ic

with open("input1.1.txt") as f:
    lines = f.readlines()

ic = generate_ic(lines)

print("Intermediate Code:")
for line in ic:
    print(line)