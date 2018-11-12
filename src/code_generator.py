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
'''

INITIAL_SEGMENT_TEXT = '''
section .text
global __start

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

__start:
    ; codigo gerado pelo compilador
'''

EXIT_SEGMENT_TEXT = '''
    ; interrupcao de saida
    MOV EAX, 1
    INT 0x80
'''

INT_VARDEC = '    {varname} ' + const.INT_REGISTER + ' 1\n'
CHAR_VARDEC = '    {varname} ' + const.CHAR_REGISTER + ' 1\n'


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

    def generate(self):
        return self.consts + self.data + self.variables + self.text + \
            EXIT_SEGMENT_TEXT
