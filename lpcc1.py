import sys 

optab = {
    "START": "AD", "END": "AD", "LTORG": "AD",
    "MOVER": "IS", "MOVEM": "IS", "ADD": "IS", "SUB": "IS", 
    "MULT": "IS", "DIV": "IS", "STOP": "IS",
    "DC": "DL", "DS": "DL"
}

registers = {"AREG": 1, "BREG": 2, "CREG": 3, "DREG": 4}

symbol_table = {}
literal_table = []
pool_table = [0]
intermediate_code = []

lc = 0

def error(msg, line_no):
    print(f"Error at line {line_no}: {msg}")
    sys.exit()   

def pass1(lines):
    global lc

    for line_no, line in enumerate(lines, start=1):
        parts = line.strip().replace(",", "").split()
        if not parts:
            continue

        if parts[0] == "START":
            if len(parts) < 2:
                error("Missing START value", line_no)
            lc = int(parts[1])
            intermediate_code.append(f"{lc} (AD,01) (C,{parts[1]})")

        elif parts[0] in ["END", "LTORG"]:
            for i in range(pool_table[-1], len(literal_table)):
                literal_table[i]["address"] = lc
                lc += 1

            pool_table.append(len(literal_table))
            intermediate_code.append(f"{lc} (AD,02)")

        else:
            if parts[0] not in optab:
                label = parts[0]

                if label in symbol_table and symbol_table[label] is not None:
                    error(f"Duplicate declaration of symbol '{label}'", line_no)

                symbol_table[label] = lc
                parts = parts[1:]

            if not parts:
                error("Missing opcode", line_no)

            opcode = parts[0]

            if opcode not in optab:
                error(f"Invalid opcode '{opcode}'", line_no)

            if opcode == "DC":
                if len(parts) < 2:
                    error("Missing value for DC", line_no)

                value = parts[1]
                intermediate_code.append(f"{lc} (DL,01) (C,{value})")
                lc += 1

            elif opcode == "DS":
                if len(parts) < 2:
                    error("Missing size for DS", line_no)

                size = int(parts[1])
                intermediate_code.append(f"{lc} (DL,02) (C,{size})")
                lc += size

            else:
                ic_line = f"{lc} ({optab[opcode]},{opcode})"

                for operand in parts[1:]:
                    if operand in registers:
                        ic_line += f" (R,{registers[operand]})"

                    elif operand.startswith("="):
                        literal_table.append({
                            "literal": operand,
                            "address": None
                        })
                        ic_line += f" (L,{len(literal_table)-1})"

                    else:
                        if operand not in symbol_table:
                            symbol_table[operand] = None  

                        ic_line += f" (S,{operand})"

                intermediate_code.append(ic_line)
                lc += 1

    for sym, addr in symbol_table.items():
        if addr is None:
            print(f"Error: Symbol '{sym}' used but not defined")
            sys.exit()

def pass2():
    print("\nINTERMEDIATE CODE")
    for line in intermediate_code:
        print(line)

def display_tables():
    print("\nSYMBOL TABLE")
    for sym, addr in symbol_table.items():
        print(sym, ":", addr)

    print("\nLITERAL TABLE")
    for i, lit in enumerate(literal_table):
        print(i, lit)

    print("\nPOOL TABLE")
    for i, p in enumerate(pool_table):
        print(i, ":", p)

with open("input1.3.txt", "r") as f:
    lines = f.readlines()

pass1(lines)
pass2()
display_tables()