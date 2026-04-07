class TokenType:
    KEYWORD = 'KEYWORD'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    FLOAT = 'FLOAT'  # Добавляем отдельный тип для чисел с плавающей точкой
    IDENTIFIER = 'IDENTIFIER'
    LPAREN = 'LPAREN'  # (
    RPAREN = 'RPAREN'  # )
    SEMICOLON = 'SEMICOLON'  # ;
    EQUALS = 'EQUALS'  # =
    PLUS = 'PLUS'  # +
    MINUS = 'MINUS'  # -
    MULTIPLY = 'MULTIPLY'  # *
    DIVIDE = 'DIVIDE'  # /
    EQ = 'EQ'  # ==
    NEQ = 'NEQ'  # !=
    LT = 'LT'  # <
    GT = 'GT'  # >
    LE = 'LE'  # <=
    GE = 'GE'  # >=
    AND = 'AND'  # and
    OR = 'OR'  # or
    NOT = 'NOT'  # not
    TRUE = 'TRUE'  # true
    FALSE = 'FALSE'  # false
    EOF = 'EOF'


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def peek_next(self, n=1):
        peek_pos = self.pos + n
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        self.advance()
        self.advance()

        while self.current_char is not None and self.current_char != '\n':
            self.advance()

        if self.current_char == '\n':
            self.advance()

    def string(self):
        result = ''
        self.advance()

        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()

        if self.current_char == '"':
            self.advance()
            return Token(TokenType.STRING, result)
        else:
            raise Exception('Незакрытая строка')

    def number(self):
        """Обработка чисел (целых и с плавающей точкой)"""
        result = ''
        dot_count = 0

        # Собираем цифры и возможную точку
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1:
                    raise Exception("Некорректное число: больше одной точки")
            result += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TokenType.NUMBER, int(result))
        else:
            return Token(TokenType.FLOAT, float(result))

    def identifier_or_keyword(self):
        result = ''
        while self.current_char is not None and (
                self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        keywords = [
            'say', 'stick', 'ask',

            'make', 'var',
            'math', 'root', 'roundUp', 'random'
            
            'number', 'string', 'float', 'logic',

            'and', 'or', 'not',

            'true', 'false',
        ]

        if result in keywords:
            if result == 'true':
                return Token(TokenType.TRUE, True)
            elif result == 'false':
                return Token(TokenType.FALSE, False)
            elif result == 'and':
                return Token(TokenType.AND, 'and')
            elif result == 'or':
                return Token(TokenType.OR, 'or')
            elif result == 'not':
                return Token(TokenType.NOT, 'not')
            else:
                return Token(TokenType.KEYWORD, result)
        else:
            return Token(TokenType.IDENTIFIER, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue

            if self.current_char == '"':
                return self.string()

            # Обработка чисел (цифры или точка в начале)
            if self.current_char.isdigit() or (self.current_char == '.' and self.peek() and self.peek().isdigit()):
                return self.number()

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.EQ, '==')

            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NEQ, '!=')

            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LE, '<=')

            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.GE, '>=')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';')

            if self.current_char == '=':
                self.advance()
                return Token(TokenType.EQUALS, '=')

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '<':
                self.advance()
                return Token(TokenType.LT, '<')

            if self.current_char == '>':
                self.advance()
                return Token(TokenType.GT, '>')

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier_or_keyword()

            raise Exception(f'Неожиданный символ: {self.current_char}')

        return Token(TokenType.EOF, None)