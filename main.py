def do_op(total, num, op):
    if op == '+':
        return total + num
    else:
        return total - num


def parse_line():
    line = input("Conta >>> ")
    i = 0
    curr = None
    num = 0
    total = 0
    op = None
    while i < len(line):
        curr = line[i]
        if curr.isspace():
            i += 1
            continue
        elif curr.isdigit():
            num *= 10
            num += int(curr)
        elif curr == '+':
            if op is not None:
                total = do_op(total, num, op)
            else:
                total = num
            op = '+'
            num = 0
        elif curr == '-':
            if op is not None:
                total = do_op(total, num, op)
            else:
                total = num
            op = '-'
            num = 0
        else:
            raise ValueError('Valor nao aceitavel: {}'.format(curr))
        i += 1
    if op is not None:
        total = do_op(total, num, op)
    return total


def run():
    while True:
        print(parse_line())


if __name__ == '__main__':
    run()
