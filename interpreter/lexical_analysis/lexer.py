from interpreter.lexical_analysis.token import Token
from interpreter.lexical_analysis.tokenType import *


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Neocekivani karakter {} '.format(self.current_char))

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def num(self, negative=False):
        number_value = '' if not negative else '-'

        while (self.current_char is not None and self.current_char.isdigit()):
            number_value += self.current_char
            self.advance()
        if self.current_char == '.':
            number_value += self.current_char
            self.advance()
            while (self.current_char is not None and self.current_char.isdigit()):
                number_value += self.current_char
                self.advance()
            return Token(DOUBLE, float(number_value))
        return Token(INT, int(number_value))

    def get_string(self):
        string_value = "'"
        self.advance()
        while self.current_char is not None and self.current_char != "'":
            string_value += self.current_char
            self.advance()
        string_value += self.current_char
        self.advance()

        return Token(STRING, string_value)

    def _id(self):
        result = ""
        while self.current_char is not None and self.current_char.isalnum() or self.current_char in ['$', '_']:
            result += self.current_char
            self.advance()

        if result == 'int':
            return Token(TYPE, result)
        if result == 'string':
            return Token(TYPE, result)
        if result == 'array':
            return Token(TYPE, result)
        if result == 'double':
            return Token(TYPE, result)
        if result == 'function':
            return Token(FUNCTION, result)
        if result == 'if':
            return Token(IF, result)
        if result == 'dont_f_stop_until':
            return Token(DONT_F_STOP_UNTIL, result)
        if result == 'return':
            return Token(RETURN, result)
        if result == 'import':
            return Token(IMPORT, result)
        if result == 'do':
            return Token(DO, result)
        if result == 'end':
            return Token(END, result)
        if result == 'and':
            return Token(AND, result)
        if result == 'or':
            return Token(OR, result)

        else:
            return Token(ID, result)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()

            # print('------')
            # print(self.current_char)
            # print('******')

            if self.current_char is None:
                return Token(EOF, None)

            if self.current_char.isdigit():
                return Token(INT, self.num())

            if self.current_char == "'":
                return self.get_string()

            if self.current_char.isalpha() or self.current_char == '$':
                return self._id()

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACKET, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACKET, '}')

            if self.current_char == '#':
                self.advance()
                return Token(HASH, '#')

            if self.current_char == '+':
                self.advance()
                if self.current_char == '+':
                    self.advance()
                    return Token(PP, '++')
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                if self.current_char == '-':
                    self.advance()
                    return Token(MM, '--')
                if self.current_char == '>':
                    self.advance()
                    return Token(ASSIGN, '->')
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '\n':
                self.advance()
                return Token(NEW_LINE, '\n')

            if self.current_char == '~':
                self.advance()
                return Token(THILDE, '~')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LESS_EQ, '<=')
                return Token(LESS, '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GREATHER_EQ, '>=')
                return Token(GREATHER, '>')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQUAL, '==')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NOT_EQUAL, '!=')
                self.error()

            self.error()

        return Token(EOF, None)
