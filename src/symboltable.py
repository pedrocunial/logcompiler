import constants as const


class Symbol(object):
    def __init__(self, value, type_):
        self.value = value
        self.type_ = type_


class SymbolTable(object):
    def __init__(self, father=None):
        self.st = {}
        self.father = father

    def add(self, type_, key):
        if key in self.st:
            raise ValueError(f'Variable name "{key}" already used')
        if key == const.RETURN:
            self.st[key] = Symbol(const.UNDEFINED, type_)
        else:
            self.st[key] = Symbol(const.DEFAULT_VALUES[type_], type_)

    def get(self, key):
        if key not in self.st:
            if self.father is not None:
                return self.father.get(key)
            else:
                raise ValueError(f'Key {key} is not in symbol table')
        return self.st[key].value

    def set(self, key, value):
        if key not in self.st:
            if self.father is not None:
                return self.father.set(key, value)
            else:
                raise ValueError(f'Undefined variable {key}')
        elif self.st[key].type_ == const.CHAR:
            if value < const.MIN_CHAR or value > const.MAX_CHAR:
                raise ValueError(f'Unmatching size of value {value} for type' +
                                 ' char')
            else:
                self.st[key].value = value
        else:
            self.st[key].value = value

    def has_return(self):
        return const.RETURN in self.st and \
            self.st[const.RETURN].value != const.UNDEFINED

    def get_return(self):
        if self.has_return():
            return self.st[const.RETURN]
        else:
            raise ValueError('Function has no return')
