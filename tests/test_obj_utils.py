#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import sys
import unittest
import traceback
import sloot.object.obj_utils as obj_utils
from sloot.object import dictobj, SimpleMultiDict
import collections


class TestMyobject(unittest.TestCase):
    """Testing myobject
    """

    def test___init__(self):
        """Testing initialisation
        """
        o = obj_utils.myobject(test1="test1", test2="test2")
        self.assertEqual(o.test1, "test1")
        self.assertEqual(o.test2, "test2")


class TestDictobj(unittest.TestCase):
    """Testing dictobject
    """

    def test___init__(self):
        """Testing __init__
        """
        # all ways to init a dict work
        # keyword arguments
        t = dictobj(a='a', b='b')
        self.assertEqual(t, {'a': 'a', 'b': 'b'})
        # a dict
        t = dictobj({'a': 'a', 'b': 'b'})
        self.assertEqual(t, {'a': 'a', 'b': 'b'})
        # an iterable
        t = dictobj([('a', 'a'), ('b', 'b')])
        self.assertEqual(t, {'a': 'a', 'b': 'b'})
        # several dicts
        t = dictobj({'a': 'a'}, {'b': 'b'})
        self.assertEqual(t, {'a': 'a', 'b': 'b'})

        # if some values are dict, they're changed to dictobj too
        t = dictobj({'a': {'b': 'b'}})
        self.assertTrue(isinstance(t.a, dictobj))

        # and it's recursive
        t = dictobj({'a': {'b': {'c': 'c'}}})
        self.assertTrue(isinstance(t.a.b, dictobj))

        # circular-referencing dicts are not supported
        orig = {}
        orig['orig'] = orig
        self.assertRaises(RuntimeError, dictobj, orig)

    def test___setitem__(self):
        """Testing __setitem__
        """
        t = dictobj()
        self.assertEqual(t._changed_values, {})

        t = dictobj({'a': 'a', 'b': 'b', 'c': 'c'})

        t.e = 'e'
        t['f'] = 'f'
        self.assertEqual(t._changed_values, {'e': 'e', 'f': 'f'})

        t.f = "new f"
        self.assertEqual(t._changed_values, {'e': 'e', 'f': "new f"})

    def test___delitem___(self):
        """Testing __delitem__
        """
        t = dictobj({'a': 'a', 'b': 'b'})

        # delitem on 'a' key
        del t['a']
        self.assertEqual(t, {'b': 'b'})
        self.assertEqual(t._deleted_keys, set('a'))

        # changed values is updated if needed
        t = dictobj()
        t.a = 'a'
        t.b = 'b'
        self.assertEqual(t._changed_values, {'a': 'a', 'b': 'b'})
        del t['a']
        self.assertEqual(t._deleted_keys, set('a'))
        self.assertEqual(t._changed_values, {'b': 'b'})

    def test_update(self):
        """Testing update
        """
        t = dictobj()
        t.update({'a': 'a', 'b': 'b', 'c': 'c'})
        self.assertEqual(t._changed_values, {'a': 'a', 'b': 'b', 'c': 'c'})

    def test_setdefault(self):
        """Testing setdefault
        """
        t = dictobj()
        t.setdefault('a', 'a')
        self.assertEqual(t.a, 'a')
        self.assertEqual(t._changed_values, {'a': 'a'})

    def test_clear(self):
        """Testing clear
        """
        t = dictobj({'a': 'a', 'b': 'b'})
        t.clear()
        self.assertEqual(t._changed_values, {})
        self.assertEqual(t._deleted_keys, set(['a', 'b']))

    def test___getattribute__(self):
        """Testing __getattribute__
        """
        class T(dictobj):

            @property
            def b(self):
                raise KeyError('b')

            @property
            def c(self):
                raise AttributeError('c')

            @property
            def d(self):
                raise ValueError('d')

            @property
            def e(self):
                raise RuntimeError('e')

            @property
            def f(self):
                return "f"

            @property
            def h(self):
                # something here raises an attribute error
                return self.c


        t = T(a='a')

        self.assertEqual(t.a, 'a')
        self.assertRaises(KeyError, lambda: t.b)
        self.assertRaises(AttributeError, lambda: t.c)
        self.assertRaises(ValueError, lambda: t.d)
        self.assertRaises(RuntimeError, lambda: t.e)
        self.assertEqual(t.f, 'f')
        self.assertRaises(AttributeError, lambda: t.g)

        raised = False
        try:
            x = t.h
        except AttributeError:
            raised = True
            stk = traceback.extract_tb(sys.exc_info()[2])
            # we don't hide the original attribute error
            self.assertEqual(stk[-1][3], "raise AttributeError('c')")

        assert raised

    def test___getattribute__precedence(self):
        class T(dictobj):
            a = "class a"

            def __init__(self, *args, **kwargs):
                self.b = 'object b'
                super(T, self).__init__(*args, **kwargs)

            def c(self):
                return "function c"

            @property
            def d(self):
                return "property d"

        t = T()

        self.assertTrue('a' not in t)
        self.assertTrue('b' not in t)
        self.assertTrue('c' not in t)
        self.assertTrue('d' not in t)

        self.assertEqual(t.a, "class a")
        self.assertEqual(t.b, "object b")
        self.assertTrue(callable(t.c))
        self.assertEqual(t.d, "property d")

        t.update({'a': 'a',
                  'b': 'b',
                  'c': 'c',
                  'd': 'd'})

        # now we have elts in the dict
        self.assertTrue('a' in t)
        self.assertTrue('b' in t)
        self.assertTrue('c' in t)
        self.assertTrue('d' in t)

        # properties still go to the class/object elements
        self.assertEqual(t.a, "class a")
        self.assertEqual(t.b, "object b")
        self.assertTrue(callable(t.c))
        self.assertEqual(t.d, "property d")

    def test___setattr__(self):
        """Testing __setattr__
        """
        class T(dictobj):
            def __init__(self, *args, **kwargs):
                self.test = 'test'
                super(T, self).__init__(*args, **kwargs)

        t = T({'a': 'a', 'b': 'b'})
        self.assertEqual(t, {'a': 'a', 'b': 'b'})

        # changed existing item
        t.a = "aaa"
        self.assertEqual(t, {'a': 'aaa', 'b': 'b'})

        # new item
        t.c = "c"
        self.assertEqual(t, {'a': 'aaa', 'b': 'b', 'c': 'c'})

        # object attr
        self.assertEqual(t.test, "test")
        t.test = "the test"
        self.assertEqual(t.test, "the test")
        self.assertEqual(t, {'a': 'aaa', 'b': 'b', 'c': 'c'})

        self.assertEqual(t.__dict__, {
            'test': 'the test',
            '_changed_values': {'a': 'aaa', 'c': 'c'},
            '_deleted_keys': set([]),
            '_initialized': True,
        })

    def test___setattr__class_attribute(self):
        """Testing __setattr__ for class attribute
        """
        class T(dictobj):
            a = "class a"

        t = T()

        # class attribute: setattr goes to the dict, and not the class
        # attribute
        self.assertEqual(t.a, "class a")
        self.assertTrue('a' not in t)
        t.a = "a"
        self.assertTrue('a' in t)
        self.assertEqual(t, {'a': 'a'})
        self.assertEqual(t.a, "class a")

    def test___delattr__(self):
        """Testing __delattr__
        """
        t = dictobj({'a': 'a', 'b': 'b'})

        # delitem on 'a' key
        del t.a
        self.assertEqual(t, {'b': 'b'})
        self.assertEqual(t._deleted_keys, set('a'))

        class T(dictobj):
            def __init__(self, *args, **kwargs):
                self.test = 'test'
                super(T, self).__init__(*args, **kwargs)

        t = T()
        self.assertEqual(t.test, "test")
        self.assertEqual(t, {})

        # delattr on 'test' attribute
        del t.test
        self.assertFalse(hasattr(t, 'test'))
        self.assertEqual(t, {})
        self.assertEqual(t._deleted_keys, set())

    def test_globally(self):
        """Testing dictobj
        """
        d = dictobj()
        assert str(d) == '{}'
        d.test = 'test'
        d.items = 'items'
        self.assertEqual(sorted(d.items()),
                         [('items', 'items'), ('test', 'test')])

        assert d['items'] == 'items'
        assert isinstance(d.items, collections.Callable)

        d = dictobj({'test': 'newtest', 'items': 'theitems'})
        assert 'test' in d
        assert d['test'] == 'newtest'
        assert 'items' in d

        d = dictobj([('test', 'another')], items=1, b3=34)
        assert 'b3' in d
        assert d.test == 'another'
        assert d['items'] == 1

        print(dict(d))
        print(getattr(d, 'b3'))

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
        print(dir(t))

        assert t.foo() == "hello"
        assert t.bar == "world"

        t['test'] = "mytest"
        assert t.test == "mytest"
        assert t.bar == "world"

        print(t.__dict__)


class TestSimpleMultiDict(unittest.TestCase):
    """Testing SimpleMultiDict
    """

    def test_getlist(self):
        """Testing getlist
        """
        d = SimpleMultiDict({'a': 'a', 'b': 'b'})
        # put in a list if not a list
        self.assertEqual(d.getlist('a'), ['a'])
        self.assertEqual(d.getlist('b'), ['b'])

        # if already a list, returned unchanged
        d['a'] = ['a', 'aa', 'aaa']
        self.assertEqual(d.getlist('a'), ['a', 'aa', 'aaa'])

    def test___repr__(self):
        """Testing __repr__
        """
        d = SimpleMultiDict({'a': ['a', 'aa', 'aaa'], 'b': 'b'})
        self.assertEqual(
            repr(d),
            "SimpleMultiDict({'a': ['a', 'aa', 'aaa'], 'b': 'b'})")


if __name__ == '__main__':
    unittest.main()


#EOF
