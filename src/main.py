import parser as prs

if __name__ == '__main__':
    loop = True
    while loop:
        value = input()
        if value == 'exit':
            loop = False
            continue
        parser = prs.Parser(value)
        print('{} = {}'.format(value, parser.analyze_expression()))
