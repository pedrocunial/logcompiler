import parser as prs
import constants as const
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Calculator')
    parser.add_argument('--file', dest='file', default=const.STD_FILE_NAME)

    args = parser.parse_args()

    with open(args.file, 'r') as fin:
        prs.Parser(fin.read())
        print(prs.Parser.parse())
