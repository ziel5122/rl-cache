class Cache(object):

    def __init__(self, size):
        self.size = size
        self.addr = [-1] * size
        self.data = [0.0] * size

    def lookup(self, i):
        try:
            return self.data[self.addr.index(i)]
        except ValueError:
            return -1