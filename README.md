# logcompiler

### Rodando o programa

O programa foi feito com python 3.6 em mente, não existe garantia de funcionamento completo em para outras versões do mesmo.

Além disso, o programa exige a depende da existência da biblioteca [argparse](https://docs.python.org/3/library/argparse.html).

Para executar o programa, basta rodar o arquivo [/src/main/py](/src/main.py). O arquivo aceita a flag `--file` como argumento (opcional). Como padrão, ele utiliza o arquivo de entrada [/examples/example.c](/examples/example.c). Além disso, foi adicionado um arquivo novo, o [/examples/type_error.c](/examples/type_error.c); a sua execucao deve resultar em um erro relativo à atribuicao erronea de dados (devido ao seu tipo).

### Diagrama Sintático

![](img/diagrama_c.png)


### EBNF

```
program = {funcdec};
funcdec = type, varname, '(', [expr, {',' expr}], ')', stmts;
funccall = varname, '(', [expr, {',', expr}], ')';
type = ('int' | 'char' | 'void');
logic_stmt = expr, ('==' | '>' | '<'), expr;
logic_expr = logic_term, {'||', logic_term};
logic_term = logic_factor, {'&&', logic_factor};
logic_factor = ('!', logic_factor) | logic_stmt;
if = 'if', '(', logic_expr, ')', stmt, ['else', stmt];
while = 'while', '(', logic_expr, ')', stmt;
stmts = '{', stmt, ';', {stmt, ';'}, '}';
stmt = print | atribuicao | stmts | if | while | vardec | funcdec | return;
return = 'return', expr;
vardec = type, varname, {',', varname};
atribuicao = varname, '=', expr;
print = 'printf', '(', expr, ')';
expr = term, {('+' | '-'), term};
term = factor, {('*' | '/'), factor};
factor = varname | (('+' | '-') factor) | (num) | ('(', expr, ')') | scanf | funccall;
scanf = 'scanf', '(', ')';
num = digit, {digit};
varname = char, {(char | digit | '_')};
digit = (0..9);
char = (a..Z);
```
