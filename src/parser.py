import constants as const
import node as nd

from tokenizer import Tokenizer
from symboltable import SymbolTable


class Parser:
    tok = None  # static attr

    def __init__(self, src):
        Parser.tok = Tokenizer(src)
        Parser.tok.get_next()

    def is_valid(value):
        return value.t is not None and value.val is not None

    def analyze_fact():
        ''' analyze a factor, as defined in the README.md '''
        value = Parser.tok.get_next()
        if not Parser.is_valid(value):
            raise ValueError('Invalid token at position {} of the string o"{}"'
                             .format(Parser.tok.pos, Parser.tok.src))

        if value.t == const.OPEN_PARENT:
            # analyze expr
            result = Parser.analyze_expression()
            if Parser.tok.curr.val == const.CLOSE_PARENT:
                return result
            else:
                raise ValueError('Expected closing parentesis, instead got {}'
                                 .format(Parser.tok.curr.val))
        elif value.t in const.SIGN_OPS:
            # + or - factor
            return nd.UnOp(value.t, [Parser.analyze_fact()])
        elif value.t == const.INT:
            return nd.IntVal(value.val, [])
        elif value.t == const.VARIABLE:
            return nd.VarVal(value.val, [])
        else:
            raise ValueError(
                'Unexpected token type, expected a factor, got a {}'.format(
                    value.t))

    def analyze_term():
        ''' terms accept * and / and are "inside" expressions '''
        result = Parser.analyze_fact()
        value = Parser.tok.get_next()  # expected to be a TERM_OPS
        while Parser.is_valid(value) and value.t in const.TERM_OPS:
            result = nd.BinOp(value.t, [result, Parser.analyze_fact()])
            value = Parser.tok.get_next()
        return result

    def analyze_expression():
        '''
        expressions accept + and - and are the most "outter" math operation
        '''
        result = Parser.analyze_term()
        value = Parser.tok.curr
        while Parser.is_valid(value) and value.t in const.EXPR_OPS:
            result = nd.BinOp(value.t, [result, Parser.analyze_term()])
            value = Parser.tok.curr
        return result

    def analyze_print():
        value = Parser.tok.get_next()  # should be open_par
        if value.t != const.OPEN_PARENT:
            raise ValueError('Unexpected token type {}, expected ('
                             .format(value.t))
        result = nd.UnOp(const.PRINT, [Parser.analyze_expression()])
        value = Parser.tok.curr
        if value.t != const.CLOSE_PARENT:
            raise ValueError('Unexpected token type {}, expected )'
                             .format(value.t))
        Parser.tok.get_next()
        return result

    def analyze_attr():
        ''' attr are basically formed of variable = expr '''
        variable_name = Parser.tok.curr.val
        value = Parser.tok.get_next()  # should be assigner
        if value.t != const.ASSIGN:
            raise ValueError('Unexpected token type {}, expected ='
                             .format(value.t))
        return nd.BinOp(const.ASSIGN, [variable_name,
                                       Parser.analyze_expression()])

    def analyze_if():
        '''
        if has 3 children:
            1: Operation to be evaluated (true/false)
            2: True stmt
            3: False stmt (not mandatory, can be NoOp)
        '''
        value = Parser.tok.curr
        if value.t != const.IF:
            raise ValueError('Unexpected token type {}, expected if'
                             .format(value.t))

    def analyze_stmt():
        ''' basically, a cmd is a line of code '''
        value = Parser.tok.get_next()
        if value.t == const.VARIABLE:
            return Parser.analyze_attr()
        elif value.t == const.RESERVED_WORD and value.val == const.PRINT:
            return Parser.analyze_print()
        elif value.t == const.OPEN_BLOCK:
            return Parser.analyze_stmts()
        elif value.t == const.CLOSE_BLOCK:
            return None
        elif value.t == const.IF:
            return Parser.analyze_if()
        else:
            raise ValueError('Unexpected token type {}, expected a cmd'
                             .format(value.t))

    def analyze_stmts():
        '''
        cmds are the most outter program logic block, including multiple
        lines
        '''
        value = Parser.tok.curr
        if value.t != const.OPEN_BLOCK:
            raise ValueError('First token should be an {, not {}'
                             .format(value.t))
        stmts = [Parser.analyze_stmt()]
        value = Parser.tok.curr
        while Parser.is_valid(value) and value.t == const.SEMICOLON:
            res = Parser.analyze_stmt()
            value = Parser.tok.curr
            if res is not None:
                stmts.append(res)
        if value.t != const.CLOSE_BLOCK:
            raise ValueError('Last token of the block is a {}, not a {}'
                             .format(value.t, const.CLOSE_BLOCK))
        value = Parser.tok.get_next()
        return nd.CmdsOp(None, stmts)

    def parse():
        st = SymbolTable()
        res = Parser.analyze_stmts().eval(st)
        if Parser.is_valid(Parser.tok.curr):
            raise ValueError('Found remaning values after last block')
        return res
