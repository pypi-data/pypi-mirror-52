class X:
    __headers__: [str] = []

    def __init__(self, *strings):
        for string in strings:
            self.__headers__.append(string)

    def exists_header(self, key_name) -> bool: ...

    def __call__(self):
        return self.__headers__

    def __getitem__(self, item):
        if item > len(self.__headers__):
            raise IndexError('Item does not search')
        return self.__headers__[item]

    def __setitem__(self, key, value):
        if key > len(self.__headers__):
            raise IndexError
        self.__headers__[key] = value

    def __str__(self):
        return f'{", ".join([f"`{h}`" for h in self.__headers__])}'


class Y:
    headers: X = None

    def __init__(self, *strings):
        self.headers = X(*strings)


z = Y('Hallo', 'Welt')
print(z.headers())
print(z.headers)
print(z.headers[1])
