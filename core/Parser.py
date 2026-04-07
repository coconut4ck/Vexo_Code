
class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class LogicOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class CompareOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, value):
        self.value = value


class StringValue(AST):
    def __init__(self, value):
        self.value = value


class LogicValue(AST):
    def __init__(self, value):
        self.value = value


class Var(AST):
    def __init__(self, name):
        self.name = name


class SayCommand(AST):
    def __init__(self, text):
        self.text = text


class StickCommand(AST):
    def __init__(self, text):
        self.text = text


class MakeVarCommand(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class MathRootCommand(AST):
    def __init__(self, value):
        self.value = value

class MathRoundUpCommand(AST):
    def __init__(self, value):
        self.value = value


class AskCommand(AST):
    def __init__(self, prompt):
        self.prompt = prompt


class NumberCommand(AST):
    def __init__(self, value):
        self.value = value


class FloatCommand(AST):
    def __init__(self, value):
        self.value = value


class StringCommand(AST):
    def __init__(self, value):
        self.value = value


class LogicCommand(AST):
    def __init__(self, value):
        self.value = value


class Program(AST):
    def __init__(self):
        self.commands = []


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(f'Ошибка парсера: {message}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Ожидался токен {token_type}, получен {self.current_token.type}')

    def parse_primary(self):
        token = self.current_token

        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Num(token.value)

        elif token.type == 'FLOAT':
            self.eat('FLOAT')
            return Num(token.value)

        elif token.type == 'STRING':
            self.eat('STRING')
            return StringValue(token.value)

        elif token.type == 'TRUE':
            self.eat('TRUE')
            return LogicValue(True)

        elif token.type == 'FALSE':
            self.eat('FALSE')
            return LogicValue(False)

        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return Var(token.value)

        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node

        elif token.type == 'NOT':
            return self.parse_not_expression()

        elif token.type == 'KEYWORD':
            if token.value == 'ask':
                return self.parse_ask_command()
            elif token.value == 'number':
                return self.parse_number_command()
            elif token.value == 'float':
                return self.parse_float_command()
            elif token.value == 'string':
                return self.parse_string_command()
            elif token.value == 'logic':
                return self.parse_logic_command()
            elif token.value == 'math':
                return self.parse_math_function()

        self.error(f'Ожидалось выражение, получено {token.type}')

    def parse_not_expression(self):
        token = self.current_token
        self.eat('NOT')
        expr = self.parse_comparison()
        return UnaryOp(token, expr)

    def parse_comparison(self):
        node = self.parse_arith_expression()

        while self.current_token.type in ('EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'):
            token = self.current_token
            if token.type == 'EQ':
                self.eat('EQ')
            elif token.type == 'NEQ':
                self.eat('NEQ')
            elif token.type == 'LT':
                self.eat('LT')
            elif token.type == 'GT':
                self.eat('GT')
            elif token.type == 'LE':
                self.eat('LE')
            elif token.type == 'GE':
                self.eat('GE')

            node = CompareOp(left=node, op=token, right=self.parse_arith_expression())

        return node

    def parse_arith_expression(self):
        node = self.parse_term()

        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')

            node = BinOp(left=node, op=token, right=self.parse_term())

        return node

    def parse_term(self):
        node = self.parse_primary()

        while self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            token = self.current_token
            if token.type == 'MULTIPLY':
                self.eat('MULTIPLY')
            elif token.type == 'DIVIDE':
                self.eat('DIVIDE')

            node = BinOp(left=node, op=token, right=self.parse_primary())

        return node

    def parse_logic_expression(self):
        node = self.parse_comparison()

        while self.current_token.type in ('AND', 'OR'):
            token = self.current_token
            if token.type == 'AND':
                self.eat('AND')
            elif token.type == 'OR':
                self.eat('OR')

            node = LogicOp(left=node, op=token, right=self.parse_comparison())

        return node

    def parse_expression(self):
        return self.parse_logic_expression()

    def parse_say_command(self):
        self.eat('KEYWORD')
        self.eat('LPAREN')
        value = self.parse_expression()
        self.eat('RPAREN')
        if self.current_token.type == 'SEMICOLON':
            self.eat('SEMICOLON')
        return SayCommand(value)

    def parse_stick_command(self):
        self.eat('KEYWORD')
        self.eat('LPAREN')
        value = self.parse_expression()
        self.eat('RPAREN')
        if self.current_token.type == 'SEMICOLON':
            self.eat('SEMICOLON')
        return StickCommand(value)

    def parse_make_var_command(self):
        self.eat('KEYWORD')
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'var':
            self.eat('KEYWORD')
        else:
            self.error('Ожидалось ключевое слово var после make')

        if self.current_token.type == 'IDENTIFIER':
            name = self.current_token.value
            self.eat('IDENTIFIER')
        else:
            self.error('Ожидалось имя переменной')

        if self.current_token.type == 'EQUALS':
            self.eat('EQUALS')
        else:
            self.error('Ожидался знак =')

        value = self.parse_expression()

        if self.current_token.type == 'SEMICOLON':
            self.eat('SEMICOLON')

        return MakeVarCommand(name, value)

    def parse_math_function(self):
        self.eat('KEYWORD')

        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'root':
            self.eat('KEYWORD')

            if self.current_token.type == 'LPAREN':
                self.eat('LPAREN')
                value = self.parse_expression()
                self.eat('RPAREN')
                return MathRootCommand(value)
            else:
                value = self.parse_expression()
                return MathRootCommand(value)
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'roundUp':
            self.eat('KEYWORD')

            if self.current_token.type == 'LPAREN':
                self.eat('LPAREN')
                value = self.parse_expression()
                self.eat('RPAREN')
                return MathRoundUpCommand(value)
            else:
                value = self.parse_expression()
                return MathRoundUpCommand(value)
        else:
            self.error('Ожидалось ключевое слово после math')

    def parse_ask_command(self):
        self.eat('KEYWORD')
        self.eat('LPAREN')
        if self.current_token.type == 'STRING':
            prompt = self.current_token.value
            self.eat('STRING')
        else:
            self.error('В ask() ожидалась строка с приглашением')
        self.eat('RPAREN')
        return AskCommand(prompt)

    def parse_number_command(self):
        self.eat('KEYWORD')
        self.eat('LPAREN')
        value = self.parse_expression()
        self.eat('RPAREN')
        return NumberCommand(value)

    def parse_float_command(self):
        self.eat('KEYWORD')
        self.eat('LPAREN')
        value = self.parse_expression()
        self.eat('RPAREN')
        return FloatCommand(value)

    def parse_string_command(self):
        self.eat('KEYWORD')
        self.eat('LPAREN')
        value = self.parse_expression()
        self.eat('RPAREN')
        return StringCommand(value)

    def parse_logic_command(self):
        self.eat('KEYWORD')
        self.eat('LPAREN')
        value = self.parse_expression()
        self.eat('RPAREN')
        return LogicCommand(value)

    def parse(self):
        program = Program()

        while self.current_token.type != 'EOF':
            if self.current_token.type == 'KEYWORD':
                if self.current_token.value == 'say':
                    command = self.parse_say_command()
                elif self.current_token.value == 'stick':
                    command = self.parse_stick_command()
                elif self.current_token.value == 'make':
                    command = self.parse_make_var_command()
                else:
                    self.error(f'Неизвестная команда: {self.current_token.value}')
                program.commands.append(command)
            else:
                self.error(f'Ожидалась команда, получен {self.current_token.type}')

        return program
