import constants as const


class Token:
    operators = (const.PLUS, const.MINUS, const.DIV, const.MULT,
                 const.OPEN_PARENT, const.CLOSE_PARENT, const.ASSIGN,
                 const.OPEN_BLOCK, const.CLOSE_BLOCK, const.SEMICOLON,
                 const.LT, const.GT, const.EQUALS, const.OR[0],
                 const.AND[0], const.NOT)

    def __init__(self, t, val):
        self.t = t
        self.val = val


class EmptyToken(Token):
    operators = (None)

    def __init__(self):
        super(EmptyToken, self).__init__(None, None)
