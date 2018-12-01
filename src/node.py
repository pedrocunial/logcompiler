import constants as const

from identifier import ID
from code_generator import CodeGenerator


codegen = None


def init_codegen():
    global codegen
    codegen = CodeGenerator()


class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id_ = ID.get_new()

    def eval(self, st):
        raise ValueError('Node class should not be directly evaluated')


class CmdsOp(Node):
    def eval(self, st):
        for child in self.children:
            child.eval(st)


class TriOp(Node):
    def __init__(self, value, children):
        if len(children) != const.TRIOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.TRIOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        codegen.if_stmt(self.children, st, self.id_)
        # if self.value == const.IF:
        #     self.children[1].eval(st) if self.children[0].eval(st) \
        #         else self.children[2].eval(st)
        # else:
        #     raise ValueError('Unexpected operator {} for triop'
        #                      .format(self.value))


class BinOp(Node):
    def __init__(self, value, children):
        if len(children) != const.BINOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.BINOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval_while(self, st):
        ''' extracted because the method was too long '''
        codegen.while_op(self.children, st, self.id_)
        # while self.children[0].eval(st):
        #     self.children[1].eval(st)

    def eval(self, st):
        codegen.binop(self.value, self.children, st)
        # if self.value == const.PLUS:
        #     return self.children[0].eval(st) + self.children[1].eval(st)
        # elif self.value == const.MINUS:
        #     return self.children[0].eval(st) - self.children[1].eval(st)
        # elif self.value == const.DIV:
        #     return self.children[0].eval(st) // self.children[1].eval(st)
        # elif self.value == const.MULT:
        #     return self.children[0].eval(st) * self.children[1].eval(st)
        if self.value == const.ASSIGN:
            # st.set(self.children[0], self.children[1].eval(st))
            self.children[1].eval(st)
            codegen.assign(self.children[0], st)
        # elif self.value == const.EQUALS:
        #     return self.children[0].eval(st) == self.children[1].eval(st)
        # elif self.value == const.LT:
        #     return self.children[0].eval(st) < self.children[1].eval(st)
        # elif self.value == const.GT:
        #     return self.children[0].eval(st) > self.children[1].eval(st)
        # elif self.value == const.AND:
        #     return self.children[0].eval(st) and self.children[1].eval(st)
        # elif self.value == const.OR:
        #     return self.children[0].eval(st) or self.children[1].eval(st)
        elif self.value == const.WHILE:
            self.eval_while(st)
        elif self.value == const.DECLARE:
            for child in self.children[1]:
                st.add(self.children[0], child)
                codegen.add_variable(child, st)


class UnOp(Node):
    def __init__(self, value, children):
        if len(children) != const.UNOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.UNOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        self.children[0].eval(st)
        codegen.unop(self.value)
        # if self.value == const.PLUS:
        #     # return +self.children[0].eval(st)
        # elif self.value == const.MINUS:
        #     # return -self.children[0].eval(st)
        # elif self.value == const.PRINT:
        #     # print(self.children[0].eval(st))
        # elif self.value == const.NOT:
        #     # return not self.children[0].eval(st)
        # else:
        #     raise ValueError('Unexpected operator {} for unop'
        #                      .format(self.value))


class Scanf(Node):
    def __init__(self, value, children):
        if len(children) != const.SCANF_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.SCANF_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        return int(input('input: '))


class IntVal(Node):
    def __init__(self, value, children):
        if len(children) != const.INTVAL_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.INTVAL_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        codegen.get_num(self.value)
        # return int(self.value)


class VarVal(Node):
    def __init__(self, value, children):
        if len(children) != const.VARVAL_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.VARVAL_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        codegen.get_variable(self.value, st)
        # return st.get(self.value)


class NoOp(Node):
    def __init__(self, value=None, children=None):
        pass

    def eval(self, st):
        pass
