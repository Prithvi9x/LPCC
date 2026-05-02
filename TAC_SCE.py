import re

temp_count = 0
label_count = 0


def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t


def new_label():
    global label_count
    l = f"L{label_count}"
    label_count += 1
    return l


class TACGenerator:

    def generate(self, code):
        code = code.strip()

        if code.startswith("while"):
            return self.handle_while(code)

        elif code.startswith("for"):
            return self.handle_for(code)

        elif code.startswith("switch"):
            return self.handle_switch(code)

        elif code.startswith("do"):
            return self.handle_do_while(code)

        elif code.startswith("if"):
            return self.handle_if(code)

        else:
            return ["Unsupported construct"]

    def parse_body(self, code):
        match = re.search(r'\{(.*)\}', code, re.S)
        if not match:
            return []
        body = match.group(1)
        return [stmt.strip() for stmt in body.split(";") if stmt.strip()]

    def generate_expression(self, expr):
        result = []

        if "=" in expr:
            lhs, rhs = expr.split("=")
            lhs = lhs.strip()
            rhs = rhs.strip()

            match = re.match(r'(.*?)([\+\-\*/])(.*)', rhs)
            if match:
                op1, op, op2 = match.groups()
                t = new_temp()
                result.append(f"{t} = {op1.strip()} {op} {op2.strip()}")
                result.append(f"{lhs} = {t}")
            else:
                result.append(f"{lhs} = {rhs}")

        return result

    def handle_while(self, code):
        result = []
        cond = re.search(r'while\s*\((.*?)\)', code).group(1)
        body = self.parse_body(code)

        start = new_label()
        end = new_label()

        result.append(f"{start}:")
        result.append(f"if not ({cond}) goto {end}")

        for stmt in body:
            result.extend(self.generate_expression(stmt))

        result.append(f"goto {start}")
        result.append(f"{end}:")
        return result

    def handle_for(self, code):
        result = []
        match = re.search(r'for\s*\((.*?);(.*?);(.*?)\)', code)
        init, cond, inc = match.groups()
        body = self.parse_body(code)

        start = new_label()
        end = new_label()

        result.extend(self.generate_expression(init.strip()))

        result.append(f"{start}:")
        result.append(f"if not ({cond.strip()}) goto {end}")

        for stmt in body:
            result.extend(self.generate_expression(stmt))

        result.extend(self.generate_expression(inc.strip()))

        result.append(f"goto {start}")
        result.append(f"{end}:")
        return result

    def handle_do_while(self, code):
        result = []
        cond = re.search(r'while\s*\((.*?)\)', code).group(1)
        body = self.parse_body(code)

        start = new_label()

        result.append(f"{start}:")
        for stmt in body:
            result.extend(self.generate_expression(stmt))
        result.append(f"if ({cond}) goto {start}")

        return result
    
    def handle_switch(self, code):
        result = []

        var = re.search(r'switch\s*\((.*?)\)', code).group(1)

        case_blocks = re.findall(r'case\s+(.*?):(.*?)(?=case|default|})', code, re.S)
        default_block = re.search(r'default:(.*?)}', code, re.S)

        labels = [new_label() for _ in case_blocks]
        default_label = new_label()
        end = new_label()

        for i, (val, _) in enumerate(case_blocks):
            result.append(f"if {var} == {val.strip()} goto {labels[i]}")

        result.append(f"goto {default_label}")

        for i, (val, body) in enumerate(case_blocks):
            result.append(f"{labels[i]}:")
            statements = [s.strip() for s in body.split(";") if s.strip()]

            for stmt in statements:
                if stmt != "break":
                    result.extend(self.generate_expression(stmt))

            result.append(f"goto {end}")

        # default
        result.append(f"{default_label}:")
        if default_block:
            statements = [s.strip() for s in default_block.group(1).split(";") if s.strip()]
            for stmt in statements:
                result.extend(self.generate_expression(stmt))

        result.append(f"{end}:")
        return result

    def handle_if(self, code):
        result = []

        conditions = re.findall(r'if\s*\((.*?)\)', code)
        body = self.parse_body(code)

        labels = [new_label() for _ in conditions]
        end = new_label()

        for i, cond in enumerate(conditions):
            result.append(f"if ({cond}) goto {labels[i]}")

        result.append(f"goto {end}")

        for i in range(len(conditions)):
            result.append(f"{labels[i]}:")
            for stmt in body:
                result.extend(self.generate_expression(stmt))
            result.append(f"goto {end}")

        result.append(f"{end}:")
        return result

if __name__ == "__main__":
    tac = TACGenerator()

    code = input("Enter your code:\n")

    output = tac.generate(code)

    print("\nTHREE ADDRESS CODE")
    for line in output:
        print(line)