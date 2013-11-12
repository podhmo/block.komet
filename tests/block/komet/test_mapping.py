# -*- coding:utf-8 -*-
import unittest
from block.komet import testing

class JSONMappingTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from block.komet.mapping import install_json_mapping
        self.config.include(install_json_mapping)

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, v, name):
        from block.komet.mapping import get_mapping_function
        return get_mapping_function(self.config, v, name=name)

    def test_boolean__true(self):
        from block.komet.interfaces import IBoolean
        mapping = self._callFUT([IBoolean], name="json")
        result = mapping(True)
        self.assertEqual(result, "true")

    def test_boolean__false(self):
        from block.komet.interfaces import IBoolean
        mapping = self._callFUT([IBoolean], name="json")
        result = mapping(False)
        self.assertEqual(result, "false")

    def test_None(self):
        from block.komet.interfaces import INothing
        mapping = self._callFUT([INothing], name="json")
        result = mapping(None)
        self.assertEqual(result, "null")

    def test_string(self):
        from block.komet.interfaces import IString
        mapping = self._callFUT([IString], name="json")
        result = mapping("ababa")
        self.assertEqual(result, '"ababa"')

    def test_datetime(self):
        from block.komet.interfaces import IDateTime
        from datetime import datetime
        mapping = self._callFUT([IDateTime], name="json")
        result = mapping(datetime(2000, 1, 1))
        self.assertEqual(result, '2000-01-01T00:00:00')

