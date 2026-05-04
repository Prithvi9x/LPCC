def generate_literal_table(lines):
    littab = []
    lc = 0

    for line in lines:
        parts = line.split()
        if not parts:
            continue

        if parts[0] == "START":
            lc = int(parts[1])
            continue

        for part in parts:
            if part.startswith("='"):
                littab.append((part, None))

        lc += 1

    addr = lc
    updated = []
    for lit, _ in littab:
        updated.append((lit, addr))
        addr += 1

    return updated

with open("input1.1.txt") as f:
    lines = f.readlines()

littab = generate_literal_table(lines)

print("Literal Table:")
for i, (lit, addr) in enumerate(littab, start=1):
    print(i, lit, addr)