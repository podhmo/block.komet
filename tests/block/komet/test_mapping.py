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

    def _makeOne(self, name):
        from block.komet.mapping import get_mapping_function_factory
        return get_mapping_function_factory(self.config, name=name)

    def test_boolean__true(self):
        from block.komet.interfaces import IBoolean
        mapping = self._makeOne(name="json")([IBoolean])
        result = mapping(True)
        self.assertEqual(result, "true")

    def test_boolean__false(self):
        from block.komet.interfaces import IBoolean
        mapping = self._makeOne(name="json")([IBoolean]) 
        result = mapping(False)
        self.assertEqual(result, "false")

    def test_None(self):
        from block.komet.interfaces import INothing
        mapping = self._makeOne(name="json")([INothing])
        result = mapping(None)
        self.assertEqual(result, "null")

    def test_string(self):
        from block.komet.interfaces import IString
        mapping = self._makeOne(name="json")([IString])
        result = mapping("ababa")
        self.assertEqual(result, '"ababa"')

    def test_datetime(self):
        from block.komet.interfaces import IDateTime
        from datetime import datetime
        mapping = self._makeOne(name="json")([IDateTime])
        result = mapping(datetime(2000, 1, 1))
        self.assertEqual(result, '2000-01-01T00:00:00')

