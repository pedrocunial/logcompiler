import parser as prs

if __name__ == '__main__':
    loop = True
    while loop:
        value = input()
        if value == 'exit':
            loop = False
            continue
        prs.Parser(value)
        print('{} = {}'.format(value, prs.Parser.analyze_expression()))
