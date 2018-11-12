class ID:
    __id = 0

    def get_new():
        ret = ID.__id
        ID.__id += 1
        return ret
