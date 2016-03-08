# tree.py, basic tree data structures for information retrieval tasks,
# agp, 07/03/2016

class Tree(object):
    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def remove(self, key):
        pass


class Trie(Tree):
    def __init__(self, key, item, *args, **kwargs):
        """ inefficiently store a set of items for a given key and efficiently reTrieve them

        :param key: hashable
        :param item: hashable
        """
        super(Trie, self).__init__(*args, **kwargs)
        self.items = set()  # not necessary to add the same item twice
        self.children = None
        if key is not None:  # else the item is discarded
            if len(key) > 0:
                self.children = {key[0]: Trie(key[1:], item)}
            else:
                self.items.add(item)

    def __getitem__(self, key):
        """given a string key, return either None or the item found"""
        if key is None:
            return None
        if len(key) == 0:
            return self.items
        elif key[0] in self.children:
            node = self.children[key[0]]
            return node[key[1:]]
        return None

    def remove(self, key, item):
        """try to remove the item from the trie"""
        if key is None:
            return None
        elif len(key) == 0:
            if len(self.items) == 0:
                return None
            if item in self.items:
                return self.items.remove(item)
        else:
            if self.children is None or self.children == {}:
                return None
            if key[0] in self.children:
                node = self.children[key[0]]
                return node.remove(key[1:], item)

    def __setitem__(self, key, item):
        """given a string key, store a hashable item in the trie"""
        if key is None:
            return
        if len(key) == 0:
            self.items.add(item)
            return
        if self.children is None:
            self.children = {}  # use a dictionary
        if key[0] not in self.children:
            self.children[key[0]] = Trie(key[1:], item)
        else:
            node = self.children[key[0]]
            node[key[1:]] = item
        return