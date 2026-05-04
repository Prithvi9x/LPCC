import re

def is_number(x):
    try:
        float(x)
        return True
    except:
        return False

def evaluate(op1, operator, op2):
    op1, op2 = float(op1), float(op2)
    if operator == '+': return op1 + op2
    if operator == '-': return op1 - op2
    if operator == '*': return op1 * op2
    if operator == '/': return op1 / op2
    return None

def optimize_TAC(tac_lines):
    constants = {}
    copies = {}
    expressions = {}
    optimized = []

    for line in tac_lines:
        line = line.strip()
        if not line:
            continue

        lhs, rhs = map(str.strip, line.split('='))

        tokens = rhs.split()
        new_rhs = []
        for token in tokens:
            if token in constants:
                new_rhs.append(str(constants[token]))
            elif token in copies:
                new_rhs.append(copies[token])
            else:
                new_rhs.append(token)

        rhs = " ".join(new_rhs)
        parts = rhs.split()

        if len(parts) == 3 and is_number(parts[0]) and is_number(parts[2]):
            result = evaluate(parts[0], parts[1], parts[2])
            rhs = str(int(result) if result.is_integer() else result)
            constants[lhs] = rhs
        else:
            if len(parts) == 1:
                copies[lhs] = parts[0]
            else:
                copies.pop(lhs, None)

        if rhs in expressions:
            optimized.append(f"{lhs} = {expressions[rhs]}")
        else:
            expressions[rhs] = lhs
            optimized.append(f"{lhs} = {rhs}")

    used = set()
    for line in optimized:
        rhs = line.split('=')[1]
        for token in rhs.split():
            if not is_number(token) and token.isidentifier():
                used.add(token)

    final_code = []
    for line in reversed(optimized):
        lhs = line.split('=')[0].strip()
        if lhs in used or line == optimized[-1]:
            final_code.append(line)
            rhs = line.split('=')[1]
            for token in rhs.split():
                if token.isidentifier():
                    used.add(token)

    final_code.reverse()
    return final_code


print("Enter Three Address Code (Enter blank line to stop):")
tac = []
while True:
    line = input()
    if line.strip() == "":
        break
    tac.append(line)

optimized_code = optimize_TAC(tac)

print("\nOptimized TAC:")
for line in optimized_code:
    print(line)