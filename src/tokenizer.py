import constants as const
import token as tk


class Tokenizer:
    def __init__(self, src, pos=0, curr=None):
        self.src = src
        self.pos = pos
        self.curr = curr

    def get_next(self):
        ''' return the next token '''
        if self.pos >= len(self.src):
            return tk.EmptyToken()  # easier error handling later on

        while self.src[self.pos].isspace():
            self.pos += 1

        if self.curr is None:
            # first case (must start with number)
            self.read_int()
        else:
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
        '''' read a known operator (in tk.Token.operators) '''
        ret = tk.Token(self.src[self.pos], self.src[self.pos])
        self.pos += 1
        self.curr = ret

    def read_any(self):
        '''' generic token reader, calls specific methods '''
        curr_token = self.src[self.pos]
        if curr_token in tk.Token.operators:
            self.read_op()
        elif curr_token.isdigit():
            self.read_int()
        else:
            raise ValueError('Unexpected token {}, doesn\'t fit any known type'
                             .format(curr_token))
