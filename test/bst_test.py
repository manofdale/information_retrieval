import unittest
from ds.tree import Bst


class TestBst(unittest.TestCase):
    def test_direct_construction_string_items(self):
        Bst(None, None)
        Bst(None, "will_be_discarded")
        item = "okidoki"
        t = Bst("abc", item)
        self.assertEqual(t["abc"], set(['okidoki']))

    def test_set_item(self):
        item = "abc"
        t = Bst("abc", item)
        t["abc"] = None  # will add None to the set
        t["bcd"] = "bcd"
        t["efg"] = "efg"
        t["efgh"] = "efgh"
        t["bcd"] = "6"
        t["bcd"] = "6"  # duplicate element
        t["aaa"] = "aaa"
        self.assertEqual(t["abc"], set([None, 'abc']))
        self.assertEqual(t["efg"], set(['efg']))
        self.assertEqual(t["efgh"], set(['efgh']))
        self.assertEqual(t["aaa"], set(['aaa']))
        self.assertEqual(t["bcd"], set(['bcd', '6']))

    # @unittest.skip("naa")
    def test_remove_item(self):
        t = Bst("abc", "1")
        t["abd"] = "abd"
        t["a"] = "a"
        t["b"] = "b"
        t["b"] = "c"
        print("initial tree")
        t.print_nodes()
        print("begin deleting items")
        t.remove("a", "a")
        self.assertEqual(t["a"], None)
        self.assertEqual(t["b"], set(["b", "c"]))
        self.assertEqual(t["abd"], set(["abd"]))
        t.remove("b", "c")
        self.assertEqual(t["b"], set(["b"]))
        t.remove("abd", "abd")
        self.assertEqual(t["abd"], None)
        t.remove("abc", "2")
        self.assertEqual(t["abc"], set(["1"]))
        print("modified tree")
        t.print_nodes()
        #t.remove("b", "b")
        #self.assertEqual(t["b"], None)
        t.remove("23k")
        self.assertEqual(t["abc"], set(["1"]))
        self.assertEqual(t["b"], set(["b"]))
        #t.remove("abc")
        #self.assertEqual(t["abc"], None)
        #self.assertEqual(t["b"], set(["b"]))


if __name__ == '__main__':
    unittest.main()
