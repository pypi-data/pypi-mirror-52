from collections import namedtuple
from unittest import TestCase

from mapping_to_namedtuple import mapping_to_named_tuple


class TestMappingToNamedTuple(TestCase):
    def test_convert_string(self):
        obj = "text"
        namedtup = mapping_to_named_tuple(obj, "root")

        expected = obj

        self.assertEqual(expected, namedtup)

    def test_convert_simple_mapping(self):
        obj = {"a": "b", "c": "d"}
        namedtup = mapping_to_named_tuple(obj, "root")

        NamedTupleClass = namedtuple("root", ["a", "c"])
        expected = NamedTupleClass(a="b", c="d")

        self.assertEqual(expected, namedtup)

    def test_convert_simple_mapping_with_list(self):
        obj = {"a": "b", "c": "d", "e": [1, 2]}
        namedtup = mapping_to_named_tuple(obj, "root")

        NamedTupleClass = namedtuple("root", ["a", "c", "e"])
        expected = NamedTupleClass(a="b", c="d", e=(1, 2))

        self.assertEqual(expected, namedtup)
