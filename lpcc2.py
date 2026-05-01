import sys

MNT = {}  
MDT = []

def error(msg, line_no=None):
    if line_no:
        print(f"Error at line {line_no}: {msg}")
    else:
        print(f"Error: {msg}")
    sys.exit()

def pass1(lines):
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("MACRO"):
            parts = line.replace(",", "").split()

            if len(parts) < 2:
                error("Macro name missing", i+1)

            macro_name = parts[1]
            args = parts[2:]
            
            if macro_name in MNT:
                error(f"Duplicate macro '{macro_name}'", i+1)

            MNT[macro_name] = (len(MDT), len(args))

            ala_map = {}
            for idx, arg in enumerate(args):
                ala_map[arg] = f"#{idx}"

            i += 1

            while i < len(lines) and lines[i].strip() != "MEND":
                body_line = lines[i].strip()

                for arg in ala_map:
                    body_line = body_line.replace(arg, ala_map[arg])

                MDT.append(body_line)
                i += 1

            MDT.append("MEND")

        i += 1


def expand_macro(name, args, output, line_no):
    if name not in MNT:
        error(f"Macro '{name}' not defined", line_no)

    mdt_index, arg_count = MNT[name]

    if len(args) != arg_count:
        error(f"Wrong number of arguments for macro '{name}'", line_no)

    ALA = {f"#{i}": args[i] for i in range(arg_count)}

    print(f"\nALA for macro '{name}':")
    for k, v in ALA.items():
        print(k, "-", v)

    i = mdt_index
    while MDT[i] != "MEND":
        line = MDT[i]

        for key in ALA:
            line = line.replace(key, ALA[key])

        tokens = line.split()

        if tokens and tokens[0] in MNT:
            expand_macro(tokens[0], tokens[1:], output, line_no)
        else:
            output.append(line)

        i += 1

def pass2(lines):
    output = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        parts = line.replace(",", "").split()

        if not parts:
            i += 1
            continue

        if parts[0] == "MACRO":
            i += 1
            while i < len(lines) and lines[i].strip() != "MEND":
                i += 1
            i += 1
            continue

        # Macro call
        if parts[0] in MNT:
            expand_macro(parts[0], parts[1:], output, i+1)

        else:
            output.append(line)

        i += 1

    return output

def display():
    print("\nMNT")
    for name, val in MNT.items():
        print(name, ":", val)

    print("\nMDT")
    for i, line in enumerate(MDT):
        print(i, ":", line)

with open("input2.2.txt", "r") as f:
    lines = f.readlines()

pass1(lines)
display()
result = pass2(lines)
print("\nEXPANDED CODE")
for line in result: print(line)