import constants as const
import node as nd
import utils

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
        elif value.t == const.RESERVED_WORD and value.val == const.SCANF:
            value = Parser.tok.get_next()
            if value.t != const.OPEN_PARENT:
                raise ValueError(f'Unexpected token type {value.t}, ' +
                                 'expected (')
            value = Parser.tok.get_next()
            if value.t != const.CLOSE_PARENT:
                raise ValueError(f'Unexpected token type {value.t}, ' +
                                 'expected )')
            return nd.Scanf(value.val, [])
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
            utils.print_error(Parser)
            raise ValueError('Unexpected token type {}, expected ='
                             .format(value.t))
        return nd.BinOp(const.ASSIGN, [variable_name,
                                       Parser.analyze_expression()])

    def analyze_logic_stmt():
        ''' expr (== | > | <) expr '''
        expr = Parser.analyze_expression()
        value = Parser.tok.curr
        if value.t not in const.LOGIC_EXPR_OPS:
            utils.print_error(Parser)
            raise ValueError(f'Unexpected token type {value.t}, expected a' +
                             ' logic expression')
        operator = value.t
        return nd.BinOp(operator, [expr, Parser.analyze_expression()])

    def analyze_logic_factor():
        '''' !, logic_factor | logic_stmt '''
        value = Parser.tok.curr
        if not Parser.is_valid(value):
            raise ValueError(f'invalid token {value.val} in logic factor')
        if value.t == const.NOT:
            return nd.UnOp(const.NOT, [Parser.analyze_logic_expr()])
        else:
            return Parser.analyze_logic_stmt()

    def analyze_logic_term():
        ''' logic_factor {&&, logic_factor} '''
        result = Parser.analyze_logic_factor()
        value = Parser.tok.curr  # expected to be a TERM_OPS
        while Parser.is_valid(value) and value.t == const.AND:
            result = nd.BinOp(value.t, [result, Parser.analyze_logic_factor()])
            value = Parser.tok.curr
        return result

    def analyze_logic_expr():
        ''' logic_term {||, logic_term}  '''
        result = Parser.analyze_logic_term()
        value = Parser.tok.curr
        while Parser.is_valid(value) and value.t == const.OR:
            result = nd.BinOp(value.t, [result, Parser.analyze_logic_term()])
            value = Parser.tok.curr
        return result

    def analyze_if():
        '''
        if has 3 children:
            1: Operation to be evaluated (true/false)
            2: True stmt
            3: False stmt (not mandatory, can be NoOp)
        '''
        value = Parser.tok.get_next()
        if value.t != const.OPEN_PARENT:
            raise ValueError('Unexpected token type {}, expected ('
                             .format(value.t))
        logic = Parser.analyze_logic_expr()
        value = Parser.tok.curr
        if value.t != const.CLOSE_PARENT:
            raise ValueError('Unexpected token type {}, expected )'
                             .format(value.t))
        true_stmt = Parser.analyze_stmt()
        value = Parser.tok.curr
        if value.val == const.ELSE:
            false_stmt = Parser.analyze_stmt()
            return nd.TriOp(const.IF, [logic, true_stmt, false_stmt])
        else:
            return nd.TriOp(const.IF, [logic, true_stmt, nd.NoOp()])

    def analyze_while():
        '''
        while has 3 children:
            1: Operation to be evaluated (true/false)
            2: Loop content (stmt)
        '''
        value = Parser.tok.get_next()
        if value.t != const.OPEN_PARENT:
            raise ValueError('Unexpected token type {}, expected ('
                             .format(value.t))
        logic = Parser.analyze_logic_expr()
        value = Parser.tok.curr
        if value.t != const.CLOSE_PARENT:
            raise ValueError('Unexpected token type {}, expected )'
                             .format(value.t))
        return nd.BinOp(const.WHILE, [logic, Parser.analyze_stmt()])

    def analyze_vardec():
        ''' <type> <varname> {, <varname>} '''
        type_ = Parser.tok.curr.val
        varnames = [Parser.tok.get_next()]
        if varnames[0].t != const.VARIABLE:
            raise ValueError('Unexpected token type {}, expected variable name'
                             .format(varnames[0].t))
        value = Parser.tok.get_next()
        while Parser.is_valid(value) and value.t == const.COMMA:
            value = Parser.tok.get_next()
            if value.t != const.VARIABLE:
                raise ValueError(f'Unexpected token type {value.t}, ' +
                                 'expected variable name')
            varnames.append(value)
            value = Parser.tok.get_next()
        varnames = [varname.val for varname in varnames]
        return nd.BinOp(const.DECLARE, [type_, varnames])

    def analyze_stmt():
        ''' basically, a cmd is a line of code '''
        value = Parser.tok.get_next()
        if value.t == const.VARIABLE:
            return Parser.analyze_attr()
        elif value.t == const.OPEN_BLOCK:
            return Parser.analyze_stmts()
        elif value.t == const.CLOSE_BLOCK:
            return None
        elif value.t == const.RESERVED_WORD:
            if value.val in const.TYPES:
                return Parser.analyze_vardec()
            elif value.val == const.IF:
                return Parser.analyze_if()
            elif value.val == const.WHILE:
                return Parser.analyze_while()
            elif value.val == const.PRINT:
                return Parser.analyze_print()
            else:
                utils.print_error(Parser)
                raise ValueError('Unexpected token type {}, expected a cmd'
                                 .format(value.t))
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
            utils.print_error(Parser)
            raise ValueError('Last token of the block is a {}, not a {}'
                             .format(value.t, const.CLOSE_BLOCK))
        value = Parser.tok.get_next()
        return nd.CmdsOp(None, stmts)

    def analyze_programx():
        ''' <type> main() { <stmts> } '''
        value = Parser.tok.curr  # should be type
        if value.val not in const.TYPES:
            raise ValueError('Program doesn\'t start with a known type')
        value = Parser.tok.get_next()
        if value.val != const.MAIN:
            raise ValueError('Main function should be named main, '
                             f'not {value.val}')
        value = Parser.tok.get_next()
        if value.val != const.OPEN_PARENT:
            raise ValueError(f'Expected (, not {value.val}')
        value = Parser.tok.get_next()
        if value.val != const.CLOSE_PARENT:
            raise ValueError(f'Expected ), not {value.val}')
        Parser.tok.get_next()
        stmts = Parser.analyze_stmts()
        return stmts

    def analyze_argdec():
        ''' <type> <varname> {, <varname>} '''
        type_ = Parser.tok.curr.val
        varnames = [Parser.tok.get_next()]
        if varnames[0].t != const.VARIABLE:
            raise ValueError('Unexpected token type {}, expected variable name'
                             .format(varnames[0].t))
        Parser.tok.get_next()
        varnames = [varname.val for varname in varnames]
        return nd.BinOp(const.DECLARE, [type_, varnames])

    def analyze_funcdec():
        ''' <type> <funcname>(<funcargs>) { <stmts> } '''
        func_type = Parser.tok.curr
        if func_type.val not in const.TYPES:
            raise ValueError('Function declaration doesn\'t start' +
                             ' with a known type')
        func_type = func_type.val
        func_name = Parser.tok.get_next()
        if func_name.t == const.RESERVED_WORD:
            raise ValueError('Function name cannot be a reserved word')
        func_name = func_name.val
        value = Parser.tok.get_next()
        if value.val != const.OPEN_PARENT:
            raise ValueError(f'Expected (, not {value.val}')
        value = Parser.tok.get_next()
        args = []
        while value.val != const.CLOSE_PARENT:
            args.append(Parser.analyze_argdec())
            curr = Parser.tok.curr
            if curr.val not in (const.COMMA, const.CLOSE_PARENT):
                raise ValueError(f'Unexpected token type {curr.val},' +
                                 ' expected "," or ")"')

    def analyze_program():
        ''' loop of function declarations '''
        while Parser.is_valid(Parser.tok.curr):
            Parser.analyze_funcdec()

    def parse():
        st = SymbolTable()
        res = Parser.analyze_program()
        if Parser.is_valid(Parser.tok.curr):
            utils.print_error(Parser)
            raise ValueError('Found remaning values after last block')
        return res.eval(st)
