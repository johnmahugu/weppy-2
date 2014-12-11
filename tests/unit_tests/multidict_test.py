import unittest

from weppy.multidict import MultiDict

class MultiDictTest(unittest.TestCase):
    def setUp(self):
        self.empty_multidict = MultiDict()

        self.multidict_items = [('a', 1), ('b', 2), ('a', 3)]
        self.multidict = MultiDict(self.multidict_items)

    def test_init(self):
        self.assertEqual(self.empty_multidict._items, [])
        self.assertEqual(self.multidict._items, self.multidict_items)
        self.assertFalse(self.multidict._items is self.multidict_items)

    def test_str(self):
        self.assertEqual(str(self.empty_multidict), '[]')
        self.assertEqual(str(self.multidict), "[('a', 1), ('b', 2), ('a', 3)]")

    def test_repr(self):
        self.assertEqual(repr(self.empty_multidict), '[]')
        self.assertEqual(repr(self.multidict), "[('a', 1), ('b', 2), ('a', 3)]")

    def test_eq(self):
        empty_multidict = MultiDict()
        self.assertEqual(self.empty_multidict, empty_multidict)

        multidict = MultiDict(self.multidict_items)
        self.assertEqual(self.multidict, multidict)

    def test_getitem(self):
        self.assertIn(self.multidict['a'], [1, 3])
        self.assertEqual(self.multidict['b'], 2)
        self.assertRaises(KeyError, self.multidict.__getitem__, 'c')

    def test_setitem(self):
        self.multidict['b'] = 4
        self.multidict['a'] = 5
        self.assertEqual(self.multidict._items,
                         [('a', 1), ('b', 2), ('a', 3), ('b', 4), ('a', 5)])

    def test_delitem(self):
        del self.multidict['a']
        self.assertEqual(self.multidict._items, [('b', 2)])

        self.assertRaises(KeyError, self.multidict.__delitem__, 'c')

    def test_contains(self):
        self.assertTrue('a' in self.multidict)
        self.assertFalse('c' in self.multidict)

    def test_len(self):
        self.assertEqual(len(self.empty_multidict), 0)
        self.assertEqual(len(self.multidict), 3)

    def test_copy(self):
        multidict = self.multidict.copy()
        self.assertEqual(multidict._items, self.multidict._items)
        self.assertFalse(multidict._items is self.multidict._items)

    def test_clear(self):
        self.multidict.clear()
        self.assertEqual(self.multidict._items, [])

    def test_get(self):
        self.assertIn(self.multidict.get('a'), [1, 3])
        self.assertEqual(self.multidict.get('b'), 2)
        self.assertEqual(self.multidict.get('c'), None)
        self.assertEqual(self.multidict.get('c', 4), 4)

    def test_getall(self):
        self.assertEqual(self.multidict.getall('a'), [1, 3])
        self.assertEqual(self.multidict.getall('b'), [2])
        self.assertEqual(self.multidict.getall('c'), [])

    def test_keys(self):
        self.assertEqual(self.empty_multidict.keys(), [])
        self.assertEqual(set(self.multidict.keys()), set(['a', 'b']))

    def test_items(self):
        self.assertEqual(self.empty_multidict.items(),
                         self.empty_multidict._items)
        self.assertFalse(self.empty_multidict.items() is
                         self.empty_multidict._items)

        self.assertEqual(self.multidict.items(), self.multidict._items)
        self.assertFalse(self.multidict.items() is self.multidict._items)

    def test_update(self):
        self.empty_multidict.update(self.multidict)
        self.assertEqual(self.empty_multidict._items,
                         self.multidict_items)

if __name__ == '__main__':
    unittest.main()
