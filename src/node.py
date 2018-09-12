import constants as const


class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self, st):
        raise ValueError('Node class should not be directly evaluated')


class CmdsOp(Node):
    def eval(self, st):
        for child in self.children:
            if child is None:
                print('child is none xd')
                continue
            child.eval(st)


class BinOp(Node):
    def __init__(self, value, children):
        if len(children) != const.BINOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.BINOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        if self.value == const.PLUS:
            return self.children[0].eval(st) + self.children[1].eval(st)
        elif self.value == const.MINUS:
            return self.children[0].eval(st) - self.children[1].eval(st)
        elif self.value == const.DIV:
            return self.children[0].eval(st) // self.children[1].eval(st)
        elif self.value == const.MULT:
            return self.children[0].eval(st) * self.children[1].eval(st)
        elif self.value == const.ASSIGN:
            st.set(self.children[0], self.children[1].eval(st))
        else:
            raise ValueError('Unexpected operator {} for binop'
                             .format(self.value))


class UnOp(Node):
    def __init__(self, value, children):
        if len(children) != const.UNOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.UNOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        if self.value == const.PLUS:
            return +self.children[0].eval(st)
        elif self.value == const.MINUS:
            return -self.children[0].eval(st)
        elif self.value == const.PRINT:
            print(self.children[0].eval(st))
        else:
            raise ValueError('Unexpected operator {} for unop'
                             .format(self.value))


class IntVal(Node):
    def __init__(self, value, children):
        if len(children) != const.INTVAL_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.INTVAL_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        return int(self.value)


class VarVal(Node):
    def __init__(self, value, children):
        if len(children) != const.VARVAL_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.VARVAL_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        return st.get(self.value)


class NoOp(Node):
    def __init__(self, value, children):
        if len(children) != const.NOOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.NOOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        pass
