
; constantes
SYS_EXIT  equ 1
SYS_READ  equ 3
SYS_WRITE equ 4
STDIN     equ 0
STDOUT    equ 1
True      equ 1
False     equ 0

segment .data

segment .bss   ; variaveis
    res RESB 1  ; usado na funcao print
    x_0 RESD 1
    y_0 RESD 1
    marcelo_0 RESB 1
    r4uL_1K3d4_0 RESB 1

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
    MOV EBX, 2
    MOV [x_0], EBX
    MOV EBX, [x_0]
    MOV [y_0], EBX
    MOV EBX, 33
    MOV [marcelo_0], EBX
    MOV EBX, 42
    NEG EBX
    MOV [r4uL_1K3d4_0], EBX
    MOV EBX, [marcelo_0]
    PUSH EBX
    CALL print

    ; interrupcao de saida
    MOV EAX, 1
    INT 0x80

