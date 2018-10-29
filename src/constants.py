from node import NoOp


PLUS = '+'
MINUS = '-'
MULT = '*'
DIV = '/'
ASSIGN = '='
SEMICOLON = ';'
UNDERSCORE = '_'
COMMA = ','
EQUALS = '=='
LT = '<'
GT = '>'
AND = '&&'
OR = '||'
NOT = '!'

IF = 'if'
ELSE = 'else'
WHILE = 'while'
INT = 'int'
CHAR = 'char'  # equivalent to bool
VOID = 'void'
OPERATOR = 'operator'
PRINT = 'printf'
SCANF = 'scanf'
RETURN = 'return'
FUNCTION = 'function'
RESERVED_WORD = 'reserved_word'
VARIABLE = 'variable'
DECLARE = 'declare'
MAIN = 'main'

DEFAULT_VALUES = {
    INT: 0,
    CHAR: 0,
    VOID: None,
    FUNCTION: NoOp()
}

AS_TYPE = {
    INT: int,
    CHAR: int,
    VOID: None
}

MIN_CHAR = -256
MAX_CHAR = 255

OPEN_PARENT = '('
CLOSE_PARENT = ')'
OPEN_BLOCK = '{'
CLOSE_BLOCK = '}'
OPEN_COMMENT = '/*'
CLOSE_COMMENT = '*/'

STD_FILE_NAME = '../examples/example.c'

TYPES = (INT, CHAR, VOID)
SIGN_OPS = (PLUS, MINUS)
TERM_OPS = (MULT, DIV)
EXPR_OPS = (PLUS, MINUS)
FACT_OPS = (OPEN_PARENT, CLOSE_PARENT)
RESERVED_WORDS = (PRINT, IF, ELSE, WHILE, SCANF, INT, CHAR, VOID, RETURN)
LOGIC_EXPR_OPS = (EQUALS, LT, GT)

TRIOP_CHILD_SIZE = 3
BINOP_CHILD_SIZE = 2
UNOP_CHILD_SIZE = 1
FUNCCALL_CHILD_SIZE = 1
FUNCDEF_CHILD_SIZE = 2
INTVAL_CHILD_SIZE = 0
VARVAL_CHILD_SIZE = 0
NOOP_CHILD_SIZE = 0
SCANF_CHILD_SIZE = 0
