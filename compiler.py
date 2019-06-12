import argparse
import textwrap

from interpreter.lexical_analysis.lexer import Lexer
from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import NodeVisitor
from interpreter.syntax_analysis.parser import Parser, Stmts


class ASTVisualizer(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.nodecount = 1
        self.num_tabs = 0
        self.dot_heder = [textwrap.dedent('from lib import *\n')]
        self.dot_body = []
        self.dot_footer = []

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Library(self, node):
        pass

    def visit_VarDecl(self, node):
        self.visit(node.type_node)
        self.visit(node.var_node)
        s = '='
        value = '\'\''
        if node.type_node.type == 'array':
            value = '[]'
        if node.type_node.type == 'int':
            value = '0'
        if node.type_node.type == 'double':
            value = '0.0'
        s += value + '\n'
        self.dot_body.append(s)

    def add_indent(self):
        self.num_tabs += 1

    def remove_indent(self):
        self.num_tabs -= 1

    def visit_Assign(self, node):
        self.visit(node.var_node)
        s = '='
        self.dot_body.append(s)
        self.visit(node.expr)
        s = '\n'
        self.dot_body.append(s)

    def visit_Return(self, node):
        s = 'return '
        self.dot_body.append(s)
        self.visit(node.node)

    def visit_FunDecl(self, node):
        s = 'def ' + node.fun_name + "("
        self.dot_body.append(s)
        self.visit(node.args_node)

        s = '):\n'

        self.dot_body.append(s)
        self.add_indent()

        self.visit(node.stmts_node)

        self.remove_indent()

    def visit_FunCall(self, node):
        s = node.fun_name[1:] if node.fun_name[0] == '$' else node.fun_name
        s += '('
        self.dot_body.append(s)

        self.visit(node.params_node)
        s = ')'
        self.dot_body.append(s)

    def visit_Loop(self, node):
        s = ''
        if node.name == DONT_F_STOP_UNTIL:
            s = 'while '
        elif node.name == IF:
            s = 'if '
        self.dot_body.append(s)

        self.visit(node.node)

        s = ':\n'
        self.dot_body.append(s)
        self.add_indent()

        self.visit(node.stmts)

        self.remove_indent()

    def visit_Args(self, node):
        for child in node.args:
            self.visit(child)
            if child != node.args[len(node.args) - 1]:
                s = ', '
                self.dot_body.append(s)

    def visit_Parms(self, node):
        for child in node.params:
            self.visit(child)
            if child != node.params[len(node.params) - 1]:
                s = ', '
                self.dot_body.append(s)

    def visit_String(self, node):
        s = node.value
        self.dot_body.append(s)

    def generate_tabs(self):
        tabs = ''
        for i in range(self.num_tabs):
            tabs = tabs + '\t'
        return tabs

    def visit_Stmts(self, node):
        for child in node.stmts:
            if not isinstance(child, Stmts):
                self.dot_body.append(self.generate_tabs())

            self.visit(child)

            if isinstance(child, Stmts):
                self.dot_body.append('\n')

    def visit_Type(self, node):
        pass

    def visit_Var(self, node):
        s = node.var
        self.dot_body.append(s)

    def visit_BinOp(self, node):
        self.dot_body.append('(')
        self.visit(node.left)
        s = node.op
        if s == '~':
            s = '+'
        self.dot_body.append(s)
        self.visit(node.right)
        self.dot_body.append(')')

    def visit_UnOp(self, node):
        if node.op == PP:
            s = node.var.var + '+=1'
        else:
            s = node.var.var + '-=1'
        self.dot_body.append(s)

    def visit_Num(self, node):
        s = str(node.value.value)
        self.dot_body.append(s)

    def genDot(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.dot_heder + self.dot_body + self.dot_footer)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fname')

    args = argparser.parse_args()
    fname = args.fname
    # fname = './examples/test1.txt'
    text = open(fname, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.genDot()

    print(content)


if __name__ == '__main__':
    main()
