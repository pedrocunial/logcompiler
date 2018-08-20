from tokenizer import Tokenizer

import token as tk
import constants as const


class Parser:
    tok = None  # static attr

    def __init__(self, src):
        Parser.tok = Tokenizer(src)

    def is_valid(value):
        return value.t is not None and value.val is not None

    def analyze_term():
        ''' terms accept * and / and are "inside" expressions '''
        value = Parser.tok.get_next()
        if not Parser.is_valid(value):
            return 0
        if value.t != const.INT:
            raise ValueError('Unexpected token type, expected int, got {}'
                             .format(value.t))

        result = value.val
        value = Parser.tok.get_next()
        while Parser.is_valid(value) and value.t in const.TERM_OPS:
            op = value.t
            value = Parser.tok.get_next()
            if value.t == const.INT:
                result = result * value.val if op == const.MULT else \
                         result // value.val
            else:
                raise ValueError('Unexpected token type, expected int, got {}'
                                 .format(value.t))
            value = Parser.tok.get_next()
        return result

    def analyze_expression():
        '''
        expressions accept + and - and are the most "outter" math operation
        '''
        # value = Parser.tok.get_next()
        # if value.t is None:
        #     # if there is no token, the final result is 0
        #     return 0

        result = Parser.analyze_term()
        value = Parser.tok.curr  # expecting our first op
        while Parser.is_valid(value):
            op = value.t
            result = result + Parser.analyze_term() if op == const.PLUS else \
                     result - Parser.analyze_term()
            value = Parser.tok.get_next()

        return result
