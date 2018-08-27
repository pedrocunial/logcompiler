# logcompiler

![](img/diagrama_c.jpg)

### Diagrama Sintático

```
expr = term, {('+' | '-'), term};
term = num, {('*' | '/'), num};
num = digit, {digit};
digit = (0..9);
```
