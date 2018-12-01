import constants as const


SYS_CONSTS = '''
; constantes
SYS_EXIT  equ 1
SYS_READ  equ 3
SYS_WRITE equ 4
STDIN     equ 0
STDOUT    equ 1
True      equ 1
False     equ 0
'''

SEGMENT_DATA = '''
segment .data
'''

SEGMENT_VARIABLES = '''
segment .bss   ; variaveis
    res RESB 1  ; usado na funcao print
'''

INITIAL_SEGMENT_TEXT = '''
section .text
global _start

print:   ; subrotina do print
    POP EBX
    POP EAX
    XOR ESI, ESI

print_dec:
    MOV EDX, 0
    MOV EBX, 0x000A
    DIV EBX
    ADD EDX, '0'
    PUSH EDX
    INC ESI
    CMP EAX, 0
    JZ print_next
    JMP print_dec

print_next:
    CMP ESI, 0
    JZ print_exit
    DEC ESI

    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT

    POP ECX
    MOV [res], ECX
    MOV ECX, res

    MOV EDX, 1
    INT 0x80
    JMP print_next

print_exit:
    RET


; subrotinas if/while
binop_je:
    JE binop_true
    JMP binop_false

binop_jg:
    JG binop_true
    JMP binop_false

binop_jl:
    JL binop_true
    JMP binop_false

binop_false:
    MOV EBX, False
    JMP binop_exit

binop_true:
    MOV EBX, True

binop_exit:
    RET

_start:
    ; codigo gerado pelo compilador
'''

EXIT_SEGMENT_TEXT = '''
    ; interrupcao de saida
    MOV EAX, 1
    INT 0x80
'''

INT_VARDEC = '    {varname} ' + const.INT_REGISTER + ' 1\n'
CHAR_VARDEC = '    {varname} ' + const.CHAR_REGISTER + ' 1\n'
ASSIGN = '    MOV [{varname}], EBX\n'
GET_VAR = '    MOV EBX, [{varname}]\n'
GET_NUM = '    MOV EBX, {num}\n'
NOT_OP = '    NOT EBX\n'
NEG_OP = '    NEG EBX\n'
PRINT_OP = '''    PUSH EBX
    CALL print
'''
PUSH_EBX = '    PUSH EBX\n'
POP_EAX = '    POP EAX\n'
SUM_OP = '    ADD EAX, EBX\n'
SUB_OP = '    SUB EAX, EBX\n'
DIV_OP = '''    MOV EDX, 0
    IDIV EBX
'''
MULT_OP = '    IMUL EBX\n'
CMP_OP = '    CMP EAX, EBX\n'
EQUALS_OP = CMP_OP + '    CALL binop_je\n'
GT_OP = CMP_OP + '    CALL binop_jg\n'
LT_OP = CMP_OP + '    CALL binop_jl\n'
AND_OP = '    AND EAX, EBX\n'
OR_OP = '    OR EAX, EBX\n'
FINISH_BINOP = '    MOV EBX, EAX\n'

CHECK_LOOP_CONDITION = '''    CMP EBX, False
    JE EXIT_{loop_id}
'''
CHECK_IF_CONDITION = '''    CMP EBX, False
    JE FALSE_{if_id}
'''
CLOSE_TRUE_STMT = '    JMP {label}\n'
CLOSE_LOOP = '''    JMP {label}
    EXIT_{label_id}
'''
FALSE_LABEL = '    FALSE_{if_id}\n'


class CodeGenerator:
    def __init__(self):
        self.consts = SYS_CONSTS
        self.data = SEGMENT_DATA
        self.variables = SEGMENT_VARIABLES
        self.text = INITIAL_SEGMENT_TEXT

    def add_variable(self, varname, st):
        var = varname + '_' + st.id_
        if st.get_type(varname) == const.INT:
            self.variables += INT_VARDEC.format(varname=var)
        elif st.get_type(varname) == const.CHAR:
            self.variables += CHAR_VARDEC.format(varname=var)
        else:
            raise ValueError(f'Unaccepted vartype {st.get_type(varname)}')

    def get_variable(self, varname, st):
        var = varname + '_' + st.id_
        self.text += GET_VAR.format(varname=var)

    def get_num(self, num):
        self.text += GET_NUM.format(num=num)

    def if_stmt(self, children, st, if_id):
        label = f'    IF_{if_id}\n'
        exit_label = f'    EXIT_{if_id}\n'
        self.text += label
        children[0].eval(st)  # if condition
        self.text += CHECK_IF_CONDITION.format(if_id=if_id)
        children[1].eval(st)  # true block
        self.text += CLOSE_TRUE_STMT.format(label=exit_label)
        self.text += FALSE_LABEL.format(if_id=if_id)
        children[2].eval(st)
        self.text += exit_label

    def while_op(self, children, st, loop_id):
        label = f'    LOOP_{loop_id}\n'
        self.text += label
        children[0].eval(st)  # loop condition
        self.text += CHECK_LOOP_CONDITION.format(loop_id=loop_id)
        children[1].eval(st)
        self.text += CLOSE_LOOP.format(label=label, label_id=loop_id)

    def unop(self, op):
        if op == const.NOT:
            self.text += NOT_OP
        elif op == const.MINUS:
            self.text += NEG_OP
        elif op == const.PRINT:
            self.text += PRINT_OP

    def binop(self, op, children, st):
        if op in (const.DECLARE, const.ASSIGN, const.WHILE):
            return
        children[0].eval(st)
        self.text += PUSH_EBX
        children[1].eval(st)
        self.text += POP_EAX
        if op == const.PLUS:
            self.text += SUM_OP
        elif op == const.MINUS:
            self.text += SUB_OP
        elif op == const.DIV:
            self.text += DIV_OP
        elif op == const.MULT:
            self.text += MULT_OP
        elif op == const.EQUALS:
            self.text += EQUALS_OP
        elif op == const.LT:
            self.text += LT_OP
        elif op == const.GT:
            self.text += GT_OP
        elif op == const.AND:
            self.text += AND_OP
        elif op == const.OR:
            self.text += OR_OP
        self.text += FINISH_BINOP

    def assign(self, varname, st):
        var = varname + '_' + st.id_
        self.text += ASSIGN.format(varname=var)

    def generate(self):
        return self.consts + self.data + self.variables + self.text + \
            EXIT_SEGMENT_TEXT
