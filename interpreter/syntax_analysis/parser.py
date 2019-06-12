from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import *
from interpreter.syntax_analysis.util import restorable


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.variables = {}

    def error(self):
        raise Exception('Error in parsing!')

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        declarations = []

        while self.current_token.type != EOF:
            if self.current_token.type == IMPORT:
                declarations.append(self.include_library())
            elif self.current_token.type == FUNCTION:
                declarations.append(self.function_declarations())
            else:
                declarations.append(self.statement_list())

        return Program(declarations)

    def include_library(self):
        self.eat(IMPORT)
        self.eat(COLON)
        library = self.current_token.value
        self.eat(ID)
        self.eat(NEW_LINE)

        return Library(library)

    def function_declarations(self):
        self.eat(FUNCTION)

        type_node = Type(self.current_token.value)
        self.eat(TYPE)

        fun_name = self.current_token.value
        self.eat(ID)

        self.eat(LPAREN)
        args_node = Args(self.argument_list())
        self.eat(RPAREN)

        self.eat(DO)
        self.eat(NEW_LINE)

        statements = []
        while self.current_token.type != END:
            statements.append(self.statement_list())

        self.eat(END)
        self.eat(NEW_LINE)
        stmts_node = Stmts(statements)

        return FunDecl(type_node=type_node, fun_name=fun_name, args_node=args_node, stmts_node=stmts_node)

    def argument_list(self):
        params = []

        while self.current_token.type != RPAREN:
            type_node = Type(self.current_token.value)
            self.eat(TYPE)

            self.eat(COLON)
            self.eat(HASH)
            var_node = Var(self.current_token.value)
            self.eat(ID)

            params.append(var_node)

            if self.current_token.type == COMMA:
                self.eat(COMMA)

        return params

    def statement_list(self):
        statements = []

        if self.check_assignment_statement():
            statements.extend(self.assignment_statement())
        elif self.current_token.type == LBRACKET:
            statements.extend(self.var_declaration())
        elif self.current_token.type == IF:
            statements.append(self.if_statement())
        elif self.current_token.type == DONT_F_STOP_UNTIL:
            statements.append(self.dont_f_stop_until_statement())
        elif self.current_token.type == RETURN:
            statements.append(self.return_statement())
        elif self.current_token.type == ID:
            statements.append(self.function_call())
            self.eat(NEW_LINE)
        elif self.current_token.type == HASH and self.check_unar_operator():
            statements.append(self.unar_operator())
            self.eat(NEW_LINE)
        else:
            self.error()
        return Stmts(statements)

    def function_call(self):
        fun_name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)

        params = []
        while self.current_token.type != RPAREN:
            if self.check_assignment_to_string() or self.current_token.type == STRING:
                node = self.string_expr()
            else:
                node = self.expr()
            params.append(node)
            if self.current_token.type == COMMA:
                self.eat(COMMA)

        self.eat(RPAREN)
        return FunCall(fun_name, Parms(params))

    def dont_f_stop_until_statement(self):
        self.eat(DONT_F_STOP_UNTIL)
        return self.loop(DONT_F_STOP_UNTIL)

    def if_statement(self):
        self.eat(IF)
        return self.loop(IF)

    def loop(self, name):
        node = self.boolean_expresion()
        self.eat(DO)
        self.eat(NEW_LINE)

        statements = []
        while self.current_token.type != END:
            statements.append(self.statement_list())

        node = Loop(node, Stmts(statements), name=name)
        self.eat(END)
        self.eat(NEW_LINE)

        return node

    @restorable
    def check_assignment_statement(self):
        while self.current_token.type != NEW_LINE:
            if self.current_token.type == ASSIGN:
                return True
            self.eat(self.current_token.type)
        return False

    def assignment_statement(self):
        declarations = []
        node = self.string_expr() if self.check_assignment_to_string() else self.expr()
        self.eat(ASSIGN)
        self.eat(HASH)
        var_node = Var(self.current_token.value)
        self.eat(ID)
        self.eat(NEW_LINE)
        assgn_node = Assign(var_node, node)
        declarations.append(assgn_node)
        return declarations

    @restorable
    def check_assignment_to_string(self):
        if self.check_assignment_statement() == False:
            return False
        while self.current_token.type != ASSIGN:
            self.eat(self.current_token.type)
        self.eat(ASSIGN)
        self.eat(HASH)
        variable = self.current_token.value
        return True if self.variables[variable] == STRING else False

    def return_statement(self):
        self.eat(RETURN)
        node = self.string_expr() if self.check_assignment_to_string() else self.expr()
        self.eat(NEW_LINE)
        node = Return(node)

        return node

    def var_declaration(self):
        declarations = []

        self.eat(LBRACKET)
        type_node = Type(self.current_token.value)
        self.eat(TYPE)
        self.eat(COMMA)
        self.eat(HASH)
        var_node = Var(self.current_token.value)
        self.eat(ID)
        self.eat(RBRACKET)

        declarations.append(VarDecl(type_node, var_node))
        self.variables[var_node.var] = type_node.type.upper()
        self.eat(NEW_LINE)

        return declarations

    @restorable
    def check_unar_operator(self):
        self.eat(HASH)
        self.eat(ID)
        return True if self.current_token.type in [MM, PP] else False

    def factor(self):
        token = self.current_token
        if token.type == INT:
            self.eat(INT)
            return Num(token)
        if token.type == DOUBLE:
            self.eat(DOUBLE)
            return Num(token)
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        if token.type == HASH:
            if self.check_unar_operator():
                return self.unar_operator()
            self.eat(HASH)
            node = Var(self.current_token.value)
            self.eat(ID)
            return node
        if token.type == ID:
            return self.function_call()

    def unar_operator(self):
        self.eat(HASH)
        var = Var(self.current_token.value)
        self.eat(ID)
        if self.current_token.type in [MM, PP]:
            node = UnOp(var, self.current_token.type)
            self.eat(self.current_token.type)
            return node
        self.error()

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(left=node, op=token.value, right=self.factor())

        return node

    def string_term(self):
        if self.current_token.type == STRING:
            node = String(self.current_token.value)
            self.eat(STRING)
            return node
        if self.current_token.type == HASH:
            self.eat(HASH)
            token = self.current_token.value
            self.eat(ID)
            return Var(token)
        if self.current_token.type == ID:
            return self.function_call()

    def string_expr(self):
        node = self.string_term()
        while self.current_token.type == THILDE:
            token = self.current_token
            self.eat(THILDE)
            node = BinOp(left=node, op=token.value, right=self.string_expr())
        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            else:
                self.error()

            node = BinOp(left=node, op=token.value, right=self.expr())

        return node

    def boolean_expresion(self):
        node = self.boolean_term()

        while self.current_token.type in (AND, OR):
            token = self.current_token
            if token.type == AND:
                self.eat(AND)
            elif token.type == OR:
                self.eat(OR)
            else:
                self.error()
            node = BinOp(left=node, op=token.value, right=self.boolean_expresion())

        return node

    def boolean_term(self):
        node = self.expr()

        while self.current_token.type in (LESS, GREATHER, EQUAL, NOT_EQUAL, LESS_EQ, GREATHER_EQ):
            op = self.current_token.value
            self.eat(self.current_token.type)
            node = BinOp(left=node, op=op, right=self.expr())
        return node

    def parse(self):
        return self.program()
