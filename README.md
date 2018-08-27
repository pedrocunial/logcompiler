# logcompiler

### Diagrama Sintático

![](img/diagrama_c.png)


### EBNF

```
expr = term, {('+' | '-'), term};
term = factor, {('*' | '/'), factor};
factor = (('+' | '-') factor) | (num) | ('(', expr, ')');
num = digit, {digit};
digit = (0..9);
```
