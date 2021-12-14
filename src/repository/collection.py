import unittest


class Collection:
    class ColIterator:
        def __init__(self, col):
            self._collection = col
            self._pos = 0

        def __next__(self):
            if self._pos == len(list(self._collection._data.keys())):
                raise StopIteration()
            self._pos += 1
            return self._collection._data[list(self._collection._data.keys())[self._pos-1]]

    def __init__(self):
        self._data = dict()

    def add(self, key, elem):
        self._data[key] = elem

    def clear(self):
        self.clear()

    @property
    def values(self):
        return list(self._data.values())

    def has_element(self, obj):
        return True if obj.id in self._data else False

    def has_id(self, id):
        return True if id in self._data.keys() else False

    def __iter__(self):
        return self.ColIterator(self)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]
