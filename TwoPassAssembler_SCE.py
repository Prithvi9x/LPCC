import re

OPTAB = {
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
    "ORIGIN": ("AD", 3),
    "EQU": ("AD", 4),
    "LTORG": ("AD", 5),

    "DC": ("DL", 1),
    "DS": ("DL", 2)
}

REG = {"AREG": 1, "BREG": 2, "CREG": 3, "DREG": 4}
COND = {"LT": 1, "LE": 2, "EQ": 3, "GT": 4, "GE": 5, "ANY": 6}

symbol_table = {}
literal_table = []
pool_table = [0]
intermediate_code = []
errors = []

def is_literal(tok):
    return re.match(r"='-?\d+'", tok)


def add_literal(lit):
    for i, entry in enumerate(literal_table):
        if entry["lit"] == lit:
            return i
    literal_table.append({"lit": lit, "addr": None})
    return len(literal_table) - 1


def assign_literals(LC):
    start = pool_table[-1]

    for i in range(start, len(literal_table)):
        if literal_table[i]["addr"] is None:
            literal_table[i]["addr"] = LC
            LC += 1

    pool_table.append(len(literal_table))
    return LC

def pass1(lines):
    LC = 0

    for line_no, line in enumerate(lines, 1):

        line = line.split("//")[0].strip()
        if not line:
            continue

        tokens = line.replace(",", "").split()

        label = None
        if tokens[0] not in OPTAB:
            label = tokens.pop(0)

            if label in symbol_table and symbol_table[label] is not None:
                errors.append(f"Line {line_no}: Duplicate symbol {label}")

            symbol_table[label] = LC

        if not tokens:
            continue

        opcode = tokens[0]

        if opcode not in OPTAB:
            errors.append(f"Line {line_no}: Invalid opcode {opcode}")
            continue

        type_, code = OPTAB[opcode]

        if opcode == "START":
            LC = int(tokens[1])
            intermediate_code.append((LC, f"(AD,{code}) (C,{tokens[1]})"))

        elif opcode in ["LTORG", "END"]:
            intermediate_code.append((LC, f"(AD,{code})"))
            LC = assign_literals(LC)

        elif opcode == "ORIGIN":
            try:
                if "+" in tokens[1]:
                    sym, offset = tokens[1].split("+")
                    LC = symbol_table[sym] + int(offset)
                else:
                    LC = symbol_table[tokens[1]]
            except:
                errors.append(f"Line {line_no}: Invalid ORIGIN")

        elif opcode == "EQU":
            try:
                symbol_table[label] = symbol_table[tokens[1]]
            except:
                errors.append(f"Line {line_no}: EQU error")

        elif opcode == "DC":
            intermediate_code.append((LC, f"(DL,1) (C,{tokens[1]})"))
            LC += 1

        elif opcode == "DS":
            size = int(tokens[1])
            intermediate_code.append((LC, f"(DL,2) (C,{size})"))
            LC += size

        else:
            IC_line = f"(IS,{code})"

            for tok in tokens[1:]:

                if is_literal(tok):
                    idx = add_literal(tok)
                    IC_line += f" (L,{idx})"

                elif tok in REG:
                    IC_line += f" (R,{REG[tok]})"

                elif tok in COND:
                    IC_line += f" (C,{COND[tok]})"

                else:
                    if tok not in symbol_table:
                        symbol_table[tok] = None
                    IC_line += f" (S,{tok})"

            intermediate_code.append((LC, IC_line))
            LC += 1

def pass2():
    machine_code = []

    for lc, code in intermediate_code:

        if "(IS" not in code:
            continue

        parts = code.split()
        opcode = parts[0][1:-1].split(",")[1]

        reg = 0
        addr = 0

        for part in parts[1:]:

            if part.startswith("(R"):
                reg = part[1:-1].split(",")[1]

            elif part.startswith("(S"):
                sym = part[1:-1].split(",")[1]
                addr = symbol_table.get(sym, 0)

            elif part.startswith("(L"):
                idx = int(part[1:-1].split(",")[1])
                addr = literal_table[idx]["addr"]

        machine_code.append(f"{lc} {opcode} {reg} {addr}")

    return machine_code

def run_assembler(filename):

    with open(filename, "r") as f:
        lines = f.readlines()

    pass1(lines)
    mc = pass2()

    print("\nSYMBOL TABLE")
    for k, v in symbol_table.items():
        if v is not None:
            print(k, ":", v)

    print("\nLITERAL TABLE")
    for i, lit in enumerate(literal_table):
        print(i, lit)

    print("\nPOOL TABLE")
    print(pool_table)

    print("\nINTERMEDIATE CODE")
    for lc, ic in intermediate_code:
        print(lc, ic)

    print("\nMACHINE CODE")
    for line in mc:
        print(line)

    print("\nERROR REPORT")
    if errors:
        for e in errors:
            print(e)
    else:
        print("No Errors Found")

if __name__ == "__main__":
    filename = input("Enter input file name: ")
    run_assembler(filename)