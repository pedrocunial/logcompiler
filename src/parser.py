from tokenizer import Tokenizer

import token as tk
import constants as const


class Parser:
    tok = None  # static attr

    def __init__(self, src):
        Parser.tok = Tokenizer(src)

    def analyze_expression(self):
        '''' do the math... duh '''
        value = Parser.tok.get_next()
        if value.t is None:
            # if there is no token, the final result is 0
            return 0

        result = value.val
        value = Parser.tok.get_next()  # expecting our first op
        while value.t in tk.Token.operators:
            op = value.t
            if op not in tk.Token.operators:
                raise ValueError('Unexpected operator {}'.format(op))

            value = Parser.tok.get_next()
            if value.t != const.INT:
                raise ValueError('Unexpected type of {}, expected an integer'
                                 .format(value.val))

            result = result + value.val if op == const.PLUS \
                     else result - value.val

            value = Parser.tok.get_next()

        return result
