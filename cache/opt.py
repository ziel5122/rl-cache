from collections import MutableMapping
from operator import itemgetter

class OPTCache(MutableMapping):
    def __init__(self, maxsize, accesses):
        self.__accesses = accesses
        self.__access_count = 0
        self.__data = dict()
        self.__size = 0
        self.__maxsize = maxsize

    def __delitem__(self, key):
        del self.__data[key]

    def __getitem__(self, key):
        self.__access_count += 1
        try:
            return self.__data[key]
        except KeyError:
            raise KeyError

    def __iter__(self):
        return iter(self.__data)

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        return '%s(%r, maxsize=%r, currsize=%r)' % (
            self.__class__.__name__,
            list(self.__data.items()),
            self.__maxsize,
            self.__size,
        )

    def __setitem__(self, key, value):
        if self.__size == self.__maxsize:
            next_accesses = dict()
            for k in self.__data.keys():
                try:
                    next_accesses[k] = self.__accesses[self.__access_count:].index(k)
                except ValueError:
                    next_accesses[k] = len(self.__accesses) + 1
            remove = sorted(next_accesses.items(), key=itemgetter(1), reverse=True)[0][0]
            del self.__data[remove]
            self.__data[key] = value
        else:
            self.__data[key] = value
            self.__size += 1

    def get_access_count(self):
        return self.__access_count

    def get_accesses(self):
        return self.__accesses

    def get_data(self):
        return self.__data

    def get_maxsize(self):
        return self.__maxsize

    def get_size(self):
        return self.__size
