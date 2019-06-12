class AST(object):
    pass


class Program(AST):
    def __init__(self, declarations):
        self.children = declarations


class Library(AST):
    def __init__(self, library):
        self.library = library


class FunDecl(AST):
    def __init__(self, type_node, fun_name, args_node, stmts_node):
        self.type_node = type_node
        self.fun_name = fun_name
        self.args_node = args_node
        self.stmts_node = stmts_node


class FunCall(AST):
    def __init__(self, fun_name, parms_node):
        self.fun_name = fun_name
        self.params_node = parms_node


class Type(AST):
    def __init__(self, type):
        self.type = type


class Var(AST):
    def __init__(self, var):
        self.var = var


class VarDecl(AST):
    def __init__(self, type_node, var_node):
        self.type_node = type_node
        self.var_node = var_node


class Assign(AST):
    def __init__(self, var_node, expr):
        self.var_node = var_node
        self.expr = expr


class String(AST):
    def __init__(self, value):
        self.value = value


class Args(AST):
    def __init__(self, args):
        self.args = args


class Parms(AST):
    def __init__(self, params):
        self.params = params


class Stmts(AST):
    def __init__(self, stmts):
        self.stmts = stmts


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnOp(AST):
    def __init__(self, var, op):
        self.var = var
        self.token = self.op = op


class Return(AST):
    def __init__(self, stmts):
        self.node = stmts


class Loop(AST):
    def __init__(self, node, stmts, name):
        self.stmts = stmts
        self.node = node
        self.name = name


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_{}'.format(type(node).__name__)
        visitor = getattr(self, method_name, self.error)
        return visitor(node)

    def error(self, node):
        raise Exception('Not found {}'.format(type(node).__name__))
