import constants as const

from identifier import ID


class Symbol(object):
    def __init__(self, value, type_):
        self.value = value
        self.type_ = type_


class SymbolTable(object):
    def __init__(self):
        self.st = {}
        self.id_ = ID.get_new()

    def add(self, type_, key):
        if key in self.st:
            raise ValueError(f'Variable name "{key}" already used')
        self.st[key] = Symbol(const.DEFAULT_VALUES[type_], type_)

    def get(self, key):
        if key not in self.st:
            raise ValueError('Key {} is not in symbol table'
                             .format(key))
        return self.st[key].value

    def get_type(self, key):
        if key not in self.st:
            raise ValueError('Key {} is not in symbol table'
                             .format(key))
        return self.st[key].type_

    def set(self, key, value):
        if key not in self.st:
            raise ValueError(f'Undefined variable {key}')
        if self.st[key].type_ == const.CHAR:
            if value < const.MIN_CHAR or value > const.MAX_CHAR:
                raise ValueError(f'Unmatching size of value {value} for type' +
                                 ' char')
            else:
                self.st[key].value = value
        else:
            self.st[key].value = value
