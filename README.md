# logcompiler

![](img/diagrama_c.png)

### Diagrama Sintático

```
expr = term, {('+' | '-'), term};
term = num, {('*' | '/'), num};
num = digit, {digit};
digit = (0..9);
```
