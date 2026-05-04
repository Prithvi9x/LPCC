import re

def precedence(op):
    if op in ('+', '-'):
        return 1
    elif op in ('*', '/'):
        return 2
    return 0

def infix_to_postfix(expr):
    stack = []
    output = []

    tokens = re.findall(r'\w+|[-+*/()]', expr)
    print(tokens)
    for token in tokens:
        if token.isalnum(): 
            output.append(token)

        elif token == '(': 
            stack.append(token)

        elif token == ')': 
            while stack and stack[-1] != '(': 
                output.append(stack.pop()) # 
            stack.pop() 

        else: 
            while stack and precedence(stack[-1]) >= precedence(token):                 
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


expr = input("Enter Expression (Example A=B+C*D): ")

left, right = expr.split('=')

postfix = infix_to_postfix(right)

stack = []
temp = 1

print("\nThree Address Code:")

for token in postfix:
    if token.isalnum():
        stack.append(token)
    else:
        op2 = stack.pop()
        op1 = stack.pop()

        t = f"T{temp}"
        temp += 1

        print(f"{t} = {op1} {token} {op2}")
        stack.append(t)

print(f"{left} = {stack.pop()}")