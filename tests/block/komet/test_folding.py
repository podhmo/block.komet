# -*- coding:utf-8 -*-
import unittest

class FlattenFoldingTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from block.komet.folding import flatten_folding
        return flatten_folding(*args, **kwargs)

    def test_it(self):
        xs = zip(["a", "b", "c", "d"], range(5))
        store = [-1, 2, -3, 4]
        def callback(r, k, i, store):
            r[k] = store[i] * store[i]
            return r

        result = self._callFUT(xs, store, {}, callback)
        self.assertEqual(
            result, 
            {"a": 1, "b": 4, "c": 9, "d": 16})

