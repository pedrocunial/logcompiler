import constants as const


class Symbol(object):
    def __init__(self, value, type_):
        self.value = value
        self.type_ = type_


class SymbolTable(object):
    def __init__(self):
        self.st = {}

    def add(self, type_, key):
        if key in self.st:
            raise ValueError(f'Variable name "{key}" already used')
        self.st[key] = Symbol(const.DEFAULT_VALUES[type_],
                              const.AS_TYPE[type_])

    def get(self, key):
        if key not in self.st:
            raise ValueError('Key {} is not in symbol table'
                             .format(key))
        return self.st[key].value

    def set(self, key, value):
        if key not in self.st:
            raise ValueError(f'Undefined variable {key}')
        elif isinstance(value, self.st[key].type_):
            self.st[key].value = value
        else:
            raise ValueError(f'Unmatching type {type(value)} and' +
                             f' {self.st[key].type_}')
