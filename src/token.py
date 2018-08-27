import constants as const


class Token:
    operators = (const.PLUS, const.MINUS, const.DIV, const.MULT,
                 const.OPEN_PARENT, const.CLOSE_PARENT)

    def __init__(self, t, val):
        self.t = t
        self.val = val


class EmptyToken(Token):
    operators = (None)

    def __init__(self):
        super(EmptyToken, self).__init__(None, None)
