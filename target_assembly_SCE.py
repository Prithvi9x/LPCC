import re

REGISTERS = ["R1", "R2", "R3", "R4"]
reg_map = {}  
free_regs = REGISTERS.copy()


def get_reg(var):
    if var in reg_map:
        return reg_map[var]

    if free_regs:
        r = free_regs.pop(0)
        reg_map[var] = r
        return r
    else:
        return REGISTERS[0]


def generate_assembly(tac_lines):
    assembly = []

    for line in tac_lines:
        line = line.strip()

        if line.endswith(":"):
            assembly.append(line)
            continue

        if line.startswith("if"):
            match = re.match(r'if (.*?) (==|!=|<|>|<=|>=) (.*?) goto (L\d+)', line)
            if match:
                op1, op, op2, label = match.groups()
                r1 = get_reg(op1)
                assembly.append(f"MOV {r1}, {op1}")
                assembly.append(f"CMP {r1}, {op2}")

                jump_map = {
                    "==": "JE",
                    "!=": "JNE",
                    "<": "JL",
                    ">": "JG",
                    "<=": "JLE",
                    ">=": "JGE"
                }
                assembly.append(f"{jump_map[op]} {label}")
            continue

        if line.startswith("goto"):
            label = line.split()[1]
            assembly.append(f"JMP {label}")
            continue

        if "=" in line:
            lhs, rhs = line.split("=")
            lhs = lhs.strip()
            rhs = rhs.strip()

            match = re.match(r'(.*?) (\+|\-|\*|/) (.*)', rhs)
            if match:
                op1, op, op2 = match.groups()
                r = get_reg(lhs)

                assembly.append(f"MOV {r}, {op1}")

                op_map = {
                    "+": "ADD",
                    "-": "SUB",
                    "*": "MUL",
                    "/": "DIV"
                }

                assembly.append(f"{op_map[op]} {r}, {op2}")
                assembly.append(f"MOV {lhs}, {r}")

            else:
                r = get_reg(lhs)
                assembly.append(f"MOV {r}, {rhs}")
                assembly.append(f"MOV {lhs}, {r}")

    return assembly

if __name__ == "__main__":
    print("Enter TAC (end with empty line):")
    tac = []

    while True:
        line = input()
        if not line:
            break
        tac.append(line)

    asm = generate_assembly(tac)

    print("\nTARGET ASSEMBLY CODE")
    for line in asm:
        print(line)