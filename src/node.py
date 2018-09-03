import constants as const


class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self):
        raise ValueError('Node class should not be directly evaluated')


class BinOp(Node):
    def __init__(self, value, children):
        if len(children) != const.BINOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.BINOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self):
        if self.value == const.PLUS:
            return self.children[0].eval() + self.children[1].eval()
        elif self.value == const.MINUS:
            return self.children[0].eval() - self.children[1].eval()
        elif self.value == const.DIV:
            return self.children[0].eval() // self.children[1].eval()
        elif self.value == const.MULT:
            return self.children[0].eval() * self.children[1].eval()
        else:
            raise ValueError('Unexpected operator {} for binop'
                             .format(self.value))


class UnOp(Node):
    def __init__(self, value, children):
        if len(children) != const.UNOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.UNOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self):
        if self.value == const.PLUS:
            return +self.children[0].eval()
        elif self.value == const.MINUS:
            return -self.children[0].eval()


class IntVal(Node):
    def __init__(self, value, children):
        if len(children) != const.INTVAL_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.INTVAL_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self):
        return int(self.value)


class NoOp(Node):
    def __init__(self, value, children):
        if len(children) != const.NOOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.NOOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self):
        pass
