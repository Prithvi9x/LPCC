def generate_symbol_table(lines):
    symtab = {}
    lc = 0

    for line in lines:
        parts = line.split()
        if not parts:
            continue

        if parts[0] == "START":
            lc = int(parts[1])
            continue

        label = None
        if len(parts) == 3:
            label = parts[0]
            opcode = parts[1]
            operand = parts[2]
        elif len(parts) == 2:
            opcode = parts[0]
            operand = parts[1]
        else:
            opcode = parts[0]
            operand = None

        if label:
            symtab[label] = lc

        if opcode == "DS":
            lc += int(operand)
        else:
            lc += 1

    return symtab

with open("input1.1.txt") as f:
    lines = f.readlines()

symtab = generate_symbol_table(lines)

print("Symbol Table:")
for i, (sym, addr) in enumerate(symtab.items(), start=1):
    print(i, sym, addr)