#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
import obj_utils
from obj_utils import dictobj


class TestMyobject(unittest.TestCase):
    """Testing myobject
    """

    def test_init(self):
        """Testing initialisation
        """
        o = obj_utils.myobject(test1="test1", test2="test2")
        self.assertEqual(o.test1, "test1")
        self.assertEqual(o.test2, "test2")


class TestDictobj(unittest.TestCase):
    """Testing dictobject
    """

    def test_globally(self):
        """Testing dictobj
        """
        d = dictobj()
        assert str(d) == '{}'
        d.test = 'test'
        d.items = 'items'
        assert d.items() == [('test', 'test'), ('items', 'items')]

        assert d['items'] == 'items'
        assert callable(d.items)

        d = dictobj({'test': 'newtest', 'items': 'theitems'})
        assert 'test' in d
        assert d['test'] == 'newtest'
        assert 'items' in d

        d = dictobj([('test', 'another')], items=1, b3=34)
        assert 'b3' in d
        assert d.test == 'another'
        assert d['items'] == 1


if __name__ == '__main__':
    unittest.main()


#EOF
