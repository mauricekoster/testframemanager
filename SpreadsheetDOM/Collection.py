# emulate a Excel VBA Collection

class Collection:

    def __init__(self):
        self.items = []
        self.itemindex = {}
        self.keyindex = []

    def Add(self, key, value):
        self.items.append(value)
        self.itemindex[key] = len(self.items) - 1
        self.keyindex.append(key)

    def Keys(self):
        pass

    def Items(self):
        pass

    def Item(self, key):
        pass

    def __getitem__(self, key):
        return self.Item(key)

    def __str__(self):
        s = "Collection(\n"
        for key in self.keyindex:
            s+= "\t%d: %s => %s\n" % (self.itemindex[key]+1 , key, self.items[self.itemindex[key]])
        s += ")"
        return s
