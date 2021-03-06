import constants as const

from symboltable import SymbolTable


class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def eval(self, st):
        raise ValueError('Node class should not be directly evaluated')


class CmdsOp(Node):
    def eval(self, st):
        for child in self.children:
            child.eval(st)
            if st.has_return():
                return st.get_return()
        return None


class VarBlock(Node):
    def eval(self, st):
        for child in self.children:
            child.eval(st)


class FuncDec(Node):
    def __init__(self, value, children):
        if len(children) != const.FUNCDEF_CHILD_SIZE:
            # 3 children: [type, args, body]
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.FUNCDEF_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        st.add(const.FUNCTION, self.value)
        st.set(self.value, self.children)


class FuncCall(Node):
    def eval(self, st):
        func_type, func_args, func_body = st.get(self.value)
        if len(func_args) != len(self.children):
            raise ValueError('Unmatching sizes between defined function args' +
                             f' and calling args ({len(func_args)} -- ' +
                             f'{len(self.children)})')
        inner_st = SymbolTable(father=st)
        if func_type != const.VOID:
            inner_st.add(func_type, const.RETURN)
        for key, value in zip(func_args, self.children):
            key.eval(inner_st)  # adds <key> to inner_st
            arg_type, arg_name = key.children
            # evals value with outter st
            inner_st.set(arg_name[0], value.eval(st))
        ret_val = func_body.eval(inner_st)
        if func_type != const.VOID and ret_val is None:
            raise ValueError('Non void function is not returning a value')
        elif func_type == const.VOID:
            return None
        elif func_type != ret_val.type_:
            raise ValueError('Miss-matched type between function and return')
        return ret_val.value


class TriOp(Node):
    def __init__(self, value, children):
        if len(children) != const.TRIOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.TRIOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval(self, st):
        if self.value == const.IF:
            self.children[1].eval(st) if self.children[0].eval(st) \
                else self.children[2].eval(st)
        else:
            raise ValueError('Unexpected operator {} for triop'
                             .format(self.value))


class BinOp(Node):
    def __init__(self, value, children):
        if len(children) != const.BINOP_CHILD_SIZE:
            raise ValueError('Wrong size for children, expected {}, got {}'
                             .format(const.BINOP_CHILD_SIZE, len(children)))
        super().__init__(value, children)

    def eval_while(self, st):
        ''' extracted because the method was too long '''
        while self.children[0].eval(st):
            self.children[1].eval(st)

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
        elif self.value == const.EQUALS:
            return self.children[0].eval(st) == self.children[1].eval(st)
        elif self.value == const.LT:
            return self.children[0].eval(st) < self.children[1].eval(st)
        elif self.value == const.GT:
            return self.children[0].eval(st) > self.children[1].eval(st)
        elif self.value == const.AND:
            return self.children[0].eval(st) and self.children[1].eval(st)
        elif self.value == const.OR:
            return self.children[0].eval(st) or self.children[1].eval(st)
        elif self.value == const.WHILE:
            self.eval_while(st)
        elif self.value == const.DECLARE:
            for child in self.children[1]:
                st.add(self.children[0], child)
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
        elif self.value == const.NOT:
            return not self.children[0].eval(st)
        elif self.value == const.RETURN:
            st.set(const.RETURN, self.children[0].eval(st))
        else:
            raise ValueError('Unexpected operator {} for unop'
                             .format(self.value))


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
    def __init__(self, value=None, children=None):
        pass

    def eval(self, st):
        pass
