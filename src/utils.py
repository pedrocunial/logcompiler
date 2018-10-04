def print_error(parser, thresh=10):
    print(parser.tok.src[parser.tok.pos-thresh:parser.tok.pos+thresh])
