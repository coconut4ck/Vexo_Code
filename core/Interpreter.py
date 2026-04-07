import math


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == 'PLUS':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            else:
                return left + right
        elif node.op.type == 'MINUS':
            self.check_numeric(left, right)
            return left - right
        elif node.op.type == 'MULTIPLY':
            self.check_numeric(left, right)
            return left * right
        elif node.op.type == 'DIVIDE':
            self.check_numeric(left, right)
            if right == 0:
                raise Exception("Деление на ноль!")
            return left / right

        raise Exception(f'Неизвестный оператор: {node.op.type}')

    def visit_CompareOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == 'EQ':
            return left == right
        elif node.op.type == 'NEQ':
            return left != right
        elif node.op.type == 'LT':
            return left < right
        elif node.op.type == 'GT':
            return left > right
        elif node.op.type == 'LE':
            return left <= right
        elif node.op.type == 'GE':
            return left >= right

        raise Exception(f'Неизвестный оператор сравнения: {node.op.type}')

    def visit_LogicOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        left_bool = self.to_bool(left)
        right_bool = self.to_bool(right)

        if node.op.type == 'AND':
            return left_bool and right_bool
        elif node.op.type == 'OR':
            return left_bool or right_bool

        raise Exception(f'Неизвестный логический оператор: {node.op.type}')

    def visit_UnaryOp(self, node):
        expr = self.visit(node.expr)
        expr_bool = self.to_bool(expr)

        if node.op.type == 'NOT':
            return not expr_bool

        raise Exception(f'Неизвестный унарный оператор: {node.op.type}')

    def to_bool(self, value):
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        elif value is None:
            return False
        else:
            return bool(value)

    def check_numeric(self, left, right):
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise Exception("Операция требует числовые операнды")

    def visit_Num(self, node):
        return node.value

    def visit_StringValue(self, node):
        return node.value

    def visit_LogicValue(self, node):
        return node.value

    def visit_Var(self, node):
        if node.name in self.variables:
            return self.variables[node.name]
        else:
            raise Exception(f"Переменная '{node.name}' не определена")

    def visit_SayCommand(self, node):
        value = self.visit(node.text)
        print(value)

    def visit_StickCommand(self, node):
        value = self.visit(node.text)
        print(value, end="")

    def visit_MakeVarCommand(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value

    def visit_MathRootCommand(self, node):
        value = self.visit(node.value)
        return math.sqrt(float(value))

    def visit_MathRoundUpCommand(self, node):
        value = self.visit(node.value)
        if isinstance(value, (int, float)):
            return round(value)
        else:
            return value

    def visit_NumberCommand(self, node):
        value = self.visit(node.value)
        try:
            if isinstance(value, bool):
                return 1 if value else 0
            elif isinstance(value, str):
                value = value.strip()
                if value.lower() in ['true', 'false']:
                    return 1 if value.lower() == 'true' else 0
                return int(float(value))
            elif isinstance(value, (int, float)):
                return int(value)
            else:
                return int(value)
        except:
            raise Exception(f"Нельзя преобразовать {value} в число")

    def visit_FloatCommand(self, node):
        value = self.visit(node.value)
        try:
            if isinstance(value, bool):
                return 1.0 if value else 0.0
            elif isinstance(value, str):
                value = value.strip()
                if value.lower() in ['true', 'false']:
                    return 1.0 if value.lower() == 'true' else 0.0
                return float(value)
            else:
                return float(value)
        except:
            raise Exception(f"Нельзя преобразовать {value} в число с плавающей точкой")

    def visit_StringCommand(self, node):
        value = self.visit(node.value)
        return str(value)

    def visit_LogicCommand(self, node):
        value = self.visit(node.value)
        return self.to_bool(value)

    def visit_AskCommand(self, node):
        user_input = input(node.prompt + " ").strip()

        if not user_input:
            return ""

        if user_input.lower() == 'true':
            return True
        elif user_input.lower() == 'false':
            return False

        try:
            if user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
                return int(user_input)
        except:
            pass

        try:
            test_str = user_input[1:] if user_input.startswith('-') else user_input
            if test_str.replace('.', '', 1).isdigit() and test_str.count('.') == 1:
                return float(user_input)
        except:
            pass

        return user_input

    def visit(self, node):
        if node is None:
            return None

        node_type = node.__class__.__name__

        if node_type == 'BinOp':
            return self.visit_BinOp(node)
        elif node_type == 'CompareOp':
            return self.visit_CompareOp(node)
        elif node_type == 'LogicOp':
            return self.visit_LogicOp(node)
        elif node_type == 'UnaryOp':
            return self.visit_UnaryOp(node)
        elif node_type == 'Num':
            return self.visit_Num(node)
        elif node_type == 'StringValue':
            return self.visit_StringValue(node)
        elif node_type == 'LogicValue':
            return self.visit_LogicValue(node)
        elif node_type == 'Var':
            return self.visit_Var(node)
        elif node_type == 'AskCommand':
            return self.visit_AskCommand(node)
        elif node_type == 'SayCommand':
            return self.visit_SayCommand(node)
        elif node_type == 'StickCommand':
            return self.visit_StickCommand(node)
        elif node_type == 'MakeVarCommand':
            return self.visit_MakeVarCommand(node)
        elif node_type == 'MathRootCommand':
            return self.visit_MathRootCommand(node)
        elif node_type == 'MathRoundUpCommand':
            return self.visit_MathRoundUpCommand(node)
        elif node_type == 'NumberCommand':
            return self.visit_NumberCommand(node)
        elif node_type == 'FloatCommand':
            return self.visit_FloatCommand(node)
        elif node_type == 'StringCommand':
            return self.visit_StringCommand(node)
        elif node_type == 'LogicCommand':
            return self.visit_LogicCommand(node)
        elif node_type == 'Program':
            for command in node.commands:
                self.visit(command)
        else:
            raise Exception(f'Неизвестный тип узла: {node_type}')

    def interpret(self):
        program = self.parser.parse()
        self.visit(program)
