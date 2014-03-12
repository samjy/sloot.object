#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
import sloot.object.obj_utils as obj_utils
from sloot.object import dictobj


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

        print dict(d)
        print getattr(d, 'b3')

    def test_inherit(self):
        """Testing inheritance
        """
        class T(dictobj):
            def foo(self):
                return "hello"

            @property
            def bar(self):
                return "world"

        t = T({'a': 1, 'b':2})
        print dir(t)

        assert t.foo() == "hello"
        assert t.bar == "world"

        t['test'] = "mytest"
        assert t.test == "mytest"
        assert t.bar == "world"

        print t.__dict__


if __name__ == '__main__':
    unittest.main()


#EOF
