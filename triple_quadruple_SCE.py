import re

temp_count = 0

def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def infix_to_postfix(expr):
    stack = []
    output = []
    tokens = re.findall(r'\w+|[()+\-*/]', expr)

    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output

def generate_TAC(postfix):
    stack = []
    tac = []

    for token in postfix:
        if token.isalnum():
            stack.append(token)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            temp = new_temp()
            tac.append((temp, op1, token, op2))
            stack.append(temp)

    return tac, stack[-1]

if __name__ == "__main__":

    print("Enter C statements (end with empty line):")

    statements = []
    while True:
        line = input()
        if not line:
            break
        statements.append(line.strip())

    all_TAC = []

    for stmt in statements:
        stmt = stmt.replace(";", "")

        if "=" in stmt:
            lhs, rhs = stmt.split("=")
            lhs = lhs.strip()
            rhs = rhs.strip()

            postfix = infix_to_postfix(rhs)
            tac, result = generate_TAC(postfix)

            all_TAC.extend(tac)
            all_TAC.append((lhs, result, '', ''))

    print("\nTHREE ADDRESS CODE")
    for res, op1, op, op2 in all_TAC:
        if op:
            print(f"{res} = {op1} {op} {op2}")
        else:
            print(f"{res} = {op1}")

    print("\nQUADRUPLE TABLE")
    print("Index\tOp\tArg1\tArg2\tResult")
    for i, (res, op1, op, op2) in enumerate(all_TAC):
        print(f"{i}\t{op}\t{op1}\t{op2}\t{res}")

    print("\nTRIPLE TABLE")
    print("Index\tOp\tArg1\tArg2")

    index_map = {}

    for i, (res, op1, op, op2) in enumerate(all_TAC):
        a1 = op1
        a2 = op2

        if op1 in index_map:
            a1 = f"({index_map[op1]})"
        if op2 in index_map:
            a2 = f"({index_map[op2]})"

        print(f"{i}\t{op}\t{a1}\t{a2}")
        index_map[res] = i