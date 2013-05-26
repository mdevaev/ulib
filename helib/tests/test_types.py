# -*- coding: utf-8 -*-


import unittest
import math

from helib import tools
import helib.tools.types # pylint: disable=W0611


##### Public classes #####
class TestTypes(unittest.TestCase) :
    def setUp(self) :
        self.__from_dict = {
            "a" : {
                "b" : {
                    "c" : (),
                    "d" : None,
                    "e" : (1, 2, 3),
                },
                "f" : {
                    "c" : 10,
                },
            },
        }
        self.__to_tuple = (
            (("a", "b", "c"), ()),
            (("a", "b", "d"), None),
            (("a", "b", "e"), (1, 2, 3)),
            (("a", "f", "c"), 10),
        )
        self.__to_plain_list = [
            ("a", [
                ('b', [
                    ('c', ()),
                    ('d', None),
                    ('e', (1, 2, 3)),
                ]),
                ('f', [('c', 10)]),
            ]),
        ]

    def test_riter(self) :
        self.assertEqual(set(tools.types.riter(self.__from_dict, 2)), set(self.__to_tuple))

    def test_has_keys_chain_true(self) :
        self.assertTrue(tools.types.hasKeysChain(self.__from_dict, ("a", "b", "c")))

    def test_has_keys_chain_false(self) :
        self.assertFalse(tools.types.hasKeysChain(self.__from_dict, ("a", "x")))

    def test_dict_to_list(self) :
        self.assertEqual(tools.types.dictToList(self.__from_dict), self.__to_plain_list)

    def test_dict_hash(self) :
        self.assertEqual(tools.types.dictHash(self.__from_dict), "bcd30033abffe688128607b606e6e3d8")

    def test_extend_replace(self) :
        self.assertEqual(
            tools.types.extendReplace(
                [1, 2, 3, 4, 5],
                3,
                [30, 40, 50],
            ),
            [1, 2, 30, 40, 50, 4, 5],
        )

    def test_chunks(self) :
       self.assertEqual(
            tools.types.chunks([1, 2, 3, 4, 5, 6, 7], 2),
            [[1, 2], [3, 4], [5, 6], [7]],
        )

    def test_pmap_one_process(self) :
        square = ( lambda arg : arg ** 2 )
        self.assertEqual(
            tools.types.pmap(math.sqrt, xrange(1000)),
            map(math.sqrt, xrange(1000)),
        )

    def test_pmap_multiprocessing(self) :
        self.assertEqual(
            tools.types.pmap(math.sqrt, xrange(1000), 10),
            map(math.sqrt, xrange(1000)),
        )

