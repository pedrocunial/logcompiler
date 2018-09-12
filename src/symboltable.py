class SymbolTable(object):
    def __init__(self):
        self.st = {}

    def get(self, key):
        if key not in self.st:
            raise ValueError('Key {} is not in symbol table'
                             .format(key))
        return self.st[key]

    def set(self, key, value):
        self.st[key] = value
