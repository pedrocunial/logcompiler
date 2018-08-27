from tokenizer import Tokenizer

import token as tk
import constants as const


class Parser:
    tok = None  # static attr

    def __init__(self, src):
        Parser.tok = Tokenizer(src)

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
            return Parser.analyze_expression() if value.val == const.PLUS \
                else -Parser.analyze_expression()
        elif value.t == const.INT:
            return value.val
        else:
            raise ValueError(
                'Unexpected token type, expected a factor, got a {}'.format(
                    value.t))

    def analyze_term():
        ''' terms accept * and / and are "inside" expressions '''
        result = Parser.analyze_fact()
        # print('#analyze_term', Parser.tok.curr.val)
        value = Parser.tok.get_next()  # expected to be a TERM_OPS
        # print('#analyze_term', Parser.tok.curr.val)
        while Parser.is_valid(value) and value.t in const.TERM_OPS:
            op = value.t
            result = result * Parser.analyze_fact() if op == const.MULT else \
                     result // Parser.analyze_fact()
            value = Parser.tok.get_next()
        return result

    def analyze_expression():
        '''
        expressions accept + and - and are the most "outter" math operation
        '''
        result = Parser.analyze_term()
        # print('#analyze_expr', Parser.tok.curr.val)
        value = Parser.tok.curr  # expecting our first op
        while Parser.is_valid(value) and value.t in const.EXPR_OPS:
            op = value.t
            result = result + Parser.analyze_term() if op == const.PLUS else \
                     result - Parser.analyze_term()
            value = Parser.tok.curr

        return result
