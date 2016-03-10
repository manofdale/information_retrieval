# tree.py, basic tree data structures for information retrieval tasks,
# agp, 07/03/2016
import logging
import copy
import random


class Tree(object):
    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def remove(self, key, item=None):
        pass


def search(tree, key):
    return tree.__getitem__(key)


class Trie(Tree):
    def __init__(self, key, item, *args, **kwargs):
        """ inefficiently store items and efficiently reTrieve them

        :param key: iterable of hashables
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

    def _find_node(self, key):
        """ search for a key in the trie

        :param key: an iterable of hashables
        :return: the trie node that is found using the key or None
        """
        if key is None:
            return None, None
        if len(key) == 0:
            return self, None
        node = self
        for k in key:
            parent = node
            if parent.children is None:
                return None, parent
            if k in parent.children:
                node = parent.children[k]
            else:
                return None, parent
        return node, parent

    def __getitem__(self, key):
        """given an iterable key, return either None or the item found

        :param key: an iterable having hashable elements
        :return: the list of items found or None
        """
        node, _ = self._find_node(key)
        if node is None:
            return None
        return node.items

    def remove(self, key, item=None):
        """try to remove the item from the trie

        :param key: find the position of the items
        :param item: to be deleted, if None delete all items
        """
        node, parent = self._find_node(key)
        if node is None:
            logging.warning("the key to be deleted: %s does not exist" % str(key))
        else:
            clean_up = False
            if item is None:
                clean_up = True
            elif item in node.items:  # just delete the item
                if len(node.items) > 1:
                    node.items.remove(item)  # remove a specific item
                else:
                    clean_up = True
            else:
                logging.warning("item to be deleted: %s does not exist" % str(item))
            if clean_up:  # clean up as much as possible
                if parent is None or (node.children is not None and node.children != {}):  # don't touch the children
                    node.items = set()
                else:
                    parent.children.pop(key[-1])  # delete the leaf node

    def __setitem__(self, key, item):
        """given an iterable key, store an item in the trie

        :param key: an iterable having hashable elements
        :param item: a hashable item
        """
        if key is None:
            logging.warning("ignoring the (None, %s) pair" % str(item))
        elif len(key) == 0:
            self.items.add(item)
            return
        if self.children is None:
            self.children = {}  # use a dictionary
        if key[0] not in self.children:
            self.children[key[0]] = Trie(key[1:], item)
        else:
            node = self.children[key[0]]
            node[key[1:]] = item


class Bst(Tree):
    def __init__(self, key, item, *args, **kwargs):
        """ efficiently store items and retrieve them slower (log n)

        :param key: iterable of hashables
        :param item: hashable
        """
        super(Bst, self).__init__(*args, **kwargs)
        self.key = key
        self.items = set()
        self.left = None
        self.right = None
        if key is not None:
            self.items.add(item)

    def _find_node(self, key):
        if key is None:
            return None, None, 0
        parent = None
        node = self
        while node is not None:
            if node.key == key:
                return node, parent, 0  # bingo
            parent = node
            if node.key > key:
                if node.left is None:
                    return node, parent, -1  # left
                node = node.left
            else:
                if node.right is None:
                    return node, parent, 1  # right
                node = node.right
        assert False  # not supposed to reach here

    def __getitem__(self, key):
        node, _, p = self._find_node(key)
        if node is None or p != 0:
            logging.warning("key %s not found" % str(key))
            return None
        return node.items  # bingo

    def __setitem__(self, key, value):
        node, _, p = self._find_node(key)
        if node is None:
            logging.warning("can not set %s to key %s" % (str(value), str(key)))
        elif p < 0:  # left
            node.left = Bst(key, value)
        elif p > 0:  # right
            node.right = Bst(key, value)
        else:  # there is already a node with the key
            node.items.add(value)

    def _append(self, node):
        parent, _, p = self._find_node(node.key)
        if p < 0:
            parent.left = node
        elif p > 0:
            parent.right = node
        else:
            logging.error("append mode does not support  duplicate keys")
            raise Exception

    def swap_data(self, move_node):
        items = self.items
        key = self.key
        self.items = move_node.items
        self.key = move_node.key
        move_node.key = key
        move_node.items = items

    def _del_node(self, parent, node):
        key = node.key
        print(node.key)
        if node.left is None and node.right is None:  # leaf node
            node.items = set()
            node.key = None
            node = None
        elif node.left is None:
            node = node.right
        elif node.right is None:
            node = node.left
        elif random.random() < 0.5:  # pick a child to swap/del
            node.key = node.left.key - 1  # since it will be discarded anyway
            node.swap_data(node.left)
            self._del_node(node, node.left)
        else:
            node.key = node.right.key + 1
            node.swap_data(node.right)
            self._del_node(node, node.right)
        if parent is not None:
            if parent.key > key:
                parent.left = node
            else:
                parent.right = node

    def print_nodes(self):
        if self.left is not None:
            self.left.print_nodes()
        print(self.key, self.items)
        if self.right is not None:
            self.right.print_nodes()

    def remove(self, key, item=None):
        """try to remove the item from the trie

        :param key: find the position of the items
        :param item: to be deleted, if None delete all items
        """
        node, parent, p = self._find_node(key)
        if node is None or p != 0:
            logging.warning("the key to be deleted: %s does not exist" % str(key))
        else:
            clean_up = False
            if item is None:
                clean_up = True
            elif item in node.items:  # just delete the item
                if len(node.items) > 1:
                    node.items.remove(item)  # remove a specific item
                else:
                    clean_up = True
            else:
                logging.warning("item to be deleted: %s does not exist" % str(item))
            if clean_up:  # clean up as much as possible
                self._del_node(parent, node)


class Avl(Bst):
    def __init__(self, *args, **kwargs):
        pass  # TODO balanced search tree
