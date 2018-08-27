# logcompiler

![](img/diagrama_c.png)

### Diagrama Sintático

```
expr = term, {('+' | '-'), term};
term = factor, {('*' | '/'), factor};
factor = (('+' | '-') factor) | (num) | ('(', expr, ')');
num = digit, {digit};
digit = (0..9);
```
