def generate_pool_table(lines):
    pooltab = [0]
    littab = []

    for line in lines:
        parts = line.split()
        for part in parts:
            if part.startswith("='"):
                littab.append(part)

        if "LTORG" in parts or "END" in parts:
            pooltab.append(len(littab))

    return pooltab

with open("input1.1.txt") as f:
    lines = f.readlines()

pooltab = generate_pool_table(lines)

print("Pool Table:")
for i, val in enumerate(pooltab):
    print(i, val)