import constants as const
import token as tk


class Tokenizer:
    def __init__(self, src, pos=0):
        self.src = src
        self.pos = pos
        self.curr = tk.EmptyToken()

    def get_next(self):
        ''' return the next token '''
        if self.pos >= len(self.src):
            self.curr = tk.EmptyToken()
            return tk.EmptyToken()  # easier error handling later on

        while self.src[self.pos].isspace():
            self.pos += 1
            if self.pos >= len(self.src):
                self.curr = tk.EmptyToken()
                return tk.EmptyToken()

        self.read_any()

        return self.curr

    def read_int(self):
        ''''
        set curr's value as the next token's value
        (in this case, an integer)
        '''
        if not self.src[self.pos].isdigit():
            # this is check is only needed when pos=0
            raise ValueError('Unexpected token {}, expected an integer'
                             .format(self.src[self.pos]))

        value = 0
        while self.src[self.pos].isdigit():
            value = value * 10 + int(self.src[self.pos])
            self.pos += 1
            if self.pos >= len(self.src):
                break

        self.curr = tk.Token(const.INT, value)

    def read_op(self):
        '''
        read a known single digit operator (in tk.Token.operators),
        such as +, - etc
        '''
        if self.src[self.pos] != const.ASSIGN or \
           self.src[self.pos+1] != const.ASSIGN:  # checks for ==
            ret = tk.Token(self.src[self.pos], self.src[self.pos])
            self.pos += 1
            self.curr = ret
        else:  # ==
            self.pos += 2
            self.curr = tk.Token(const.EQUALS, const.EQUALS)

    def is_open_comment(self):
        if self.pos + 1 < len(self.src):
            return (self.src[self.pos] + self.src[self.pos+1]) == \
                const.OPEN_COMMENT
        else:
            return False

    def is_close_comment(self):
        if self.pos + 1 < len(self.src):
            return (self.src[self.pos] + self.src[self.pos+1]) == \
                const.CLOSE_COMMENT
        else:
            return False

    def comment_loop(self):
        ''' "traps" the tokenizer while in this "comment state" '''
        src_len = len(self.src)
        while not self.is_close_comment() and self.pos < src_len:
            self.pos += 1

        self.pos += 2  # close comment uses 2 chars
        self.get_next()

    def read_word(self):
        '''
        read a word character by character, returning a node for it
        with it's type being either variable or reserved word
        a variable can only start with a character, but can have numbers
        and underscore in it
        '''
        word = self.src[self.pos]
        self.pos += 1
        while self.src[self.pos].isalpha() or self.src[self.pos].isdigit() \
              or self.src[self.pos] == const.UNDERSCORE:
            word += self.src[self.pos]
            self.pos += 1
        self.curr = tk.Token(const.RESERVED_WORD
                             if word in const.RESERVED_WORDS
                             else const.VARIABLE, word)

    def read_any(self):
        '''' generic token reader, calls specific methods '''
        curr_token = self.src[self.pos]
        if self.is_open_comment():
            self.comment_loop()
        elif curr_token in tk.Token.operators:
            self.read_op()
        elif curr_token.isdigit():
            self.read_int()
        elif curr_token.isalpha():
            self.read_word()
        else:
            raise ValueError('Unexpected token {}, doesn\'t fit any known type'
                             .format(curr_token))
