# emulate a Excel VBA Collection

class Collection:

    def __init__(self):
        self.items = []
        self.itemindex = {}
        self.keyindex = []

    def Add(self, value, key):
        self.items.append(value)
        self.itemindex[key] = len(self.items) - 1
        self.keyindex.append(key)

    def Keys(self):
        pass

    def Items(self):
        pass

    def Item(self, key):
        if type(key) is int:
            return self.items[key-1]
        else:
            return self.items[self.itemindex[key]]

    def __getitem__(self, key):
        return self.Item(key)

    def __str__(self):
        s = "Collection(\n"
        for key in self.keyindex:
            s+= "\t%d: %s => %s\n" % (self.itemindex[key]+1 , key, self.items[self.itemindex[key]])
        s += ")"
        return s


    def __iter__(self):
        return iter(self.items)

if __name__ == '__main__':
    coll = Collection()
    coll.Add(123, 'test')
    coll.Add(456, 'test2')
    print(coll)
    print(coll[1])
    print(coll['test2'])
    print('-'*10)
    for i in coll:
        print(i)
