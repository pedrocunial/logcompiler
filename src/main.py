import parser as prs

if __name__ == '__main__':
    loop = True
    while loop:
        try:
            value = input()
        except EOFError as err:
            loop = False
            continue
        if value == 'exit':
            loop = False
            continue
        prs.Parser(value)
        print('{} = {}'.format(value, prs.Parser.analyze_expression()))
