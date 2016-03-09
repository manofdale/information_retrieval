import unittest
from ds.tree import Trie


class TestTrie(unittest.TestCase):
    def test_direct_construction_string_items(self):
        Trie(None, None)
        Trie(None, "will_be_discarded")
        item = "okidoki"
        t = Trie("abc", item)
        self.assertEqual(t["abc"], set(['okidoki']))

    def test_set_item(self):
        item = "abc"
        t = Trie("abc", item)
        t["abc"] = None  # will add None to the set
        t["ab"] = "ab"
        t["acd"] = "acd"
        t["acd"] = "6"
        t["acd"] = "6"  # duplicate element
        self.assertEqual(t["abc"], set([None, 'abc']))
        self.assertEqual(t["ab"], set(['ab']))
        self.assertEqual(t["acd"], set(['acd', '6']))
        self.assertEqual(t["a"], set())

    def test_remove_item(self):
        t = Trie("abc", "1")
        t["abd"] = "abd"
        t["a"] = "a"
        t["b"] = "b"
        t["b"] = "c"
        t.remove("a", "a")
        self.assertEqual(t["a"], set())
        self.assertEqual(t["ab"], set())
        self.assertEqual(t["b"], set(["b", "c"]))
        t.remove("b", "c")
        self.assertEqual(t["b"], set(["b"]))
        t.remove("abc", "2")
        self.assertEqual(t["abc"], set(["1"]))
        t.remove("abc", "1")
        self.assertEqual(t["abc"], None)
        t["abc"] = "1"
        t["abc"] = "2"
        self.assertEqual(t["abc"], set(["1", "2"]))
        t.remove("abc")
        self.assertEqual(t["abc"], None)
        self.assertEqual(t["ab"], set())


if __name__ == '__main__':
    unittest.main()
