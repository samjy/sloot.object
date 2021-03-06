#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
import traceback
import sloot.object.obj_utils as obj_utils
from sloot.object import dictobj, SimpleMultiDict
try:
    import collections.abc as collections
except ImportError:
    import collections
import copy
import json
import pickle


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

    def test___repr__(self):
        """Testing __repr__
        """
        d = {'a': 1, 'b': 'b'}
        t = dictobj(d)
        self.assertEqual(repr(t), "dictobj(%s)" % dict.__repr__(d))

    def test___setitem__(self):
        """Testing __setitem__
        """
        t = dictobj()

        t = dictobj({'a': 'a', 'b': 'b', 'c': 'c'})

        t.e = 'e'
        t['f'] = 'f'

        t.f = "new f"
        self.assertEqual(t, {'a': 'a', 'b': 'b', 'c': 'c', 'e': 'e', 'f': "new f"})

    def test___delitem___(self):
        """Testing __delitem__
        """
        t = dictobj({'a': 'a', 'b': 'b'})

        # delitem on 'a' key
        del t['a']
        self.assertEqual(t, {'b': 'b'})

        # changed values is updated if needed
        t = dictobj()
        t.a = 'a'
        t.b = 'b'
        self.assertEqual(t, {'a': 'a', 'b': 'b'})
        del t['a']
        self.assertTrue('a' not in t)

    def test_update(self):
        """Testing update
        """
        t = dictobj()
        t.update({'a': 'a', 'b': 'b', 'c': 'c'})
        self.assertEqual(t, {'a': 'a', 'b': 'b', 'c': 'c'})

    def test_setdefault(self):
        """Testing setdefault
        """
        t = dictobj()
        t.setdefault('a', 'a')
        self.assertEqual(t.a, 'a')
        self.assertEqual(t, {'a': 'a'})

    def test_clear(self):
        """Testing clear
        """
        t = dictobj({'a': 'a', 'b': 'b'})
        t.clear()
        self.assertTrue('a' not in t)

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
            assert 0, "shouldn't be reached, but was, with x = %r" % x
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

    def test___settr__property(self):
        """Testing __setattr__ for property
        """
        class T(dictobj):

            @property
            def my_prop(self):
                return 'my_prop'

            @my_prop.setter
            def my_prop(self, value):
                self.some_key = value

        t = T({'a': 'a'})

        # getter
        self.assertEqual(t.my_prop, 'my_prop')
        # property takes precedence
        t['my_prop'] = 'some other value'
        self.assertEqual(t.my_prop, 'my_prop')

        # setter
        self.assertTrue('some_key' not in t)
        t.my_prop = 'setting my_prop'
        # property is still there
        self.assertEqual(t.my_prop, 'my_prop')
        # dict value is unchanged
        self.assertEqual(t['my_prop'], 'some other value')
        # the setter ran properly
        self.assertEqual(t.some_key, 'setting my_prop')

    def test___delattr__(self):
        """Testing __delattr__
        """
        t = dictobj({'a': 'a', 'b': 'b'})

        # delitem on 'a' key
        del t.a
        self.assertEqual(t, {'b': 'b'})

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

    def test_globally(self):
        """Testing dictobj
        """
        d = dictobj()
        assert str(d) == 'dictobj({})'
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

        t = T({'a': 1, 'b': 2})
        print(dir(t))

        assert t.foo() == "hello"
        assert t.bar == "world"

        t['test'] = "mytest"
        assert t.test == "mytest"
        assert t.bar == "world"

        print(t.__dict__)

    def test_json(self):
        """Testing dictobj json serialization
        """
        data = json.dumps(dictobj(a=1, b=2, c="d"), sort_keys=True)
        self.assertEqual(data, u'{"a": 1, "b": 2, "c": "d"}')

    def test_pickle(self):
        """Testing dictobj pickle
        """
        d = dictobj({'a': 1, 'b': "c", 'd': dictobj(x="y")})
        ret = pickle.dumps(d)
        assert ret
        d2 = pickle.loads(ret)
        assert d2 == d
        assert d2.__dict__ == d.__dict__

    def test_copy(self):
        """Testing copy
        """
        d1 = dictobj({'a': 'a', 'b': 'b'})
        d2 = d1.copy()
        assert d1 == d2
        assert d1 is not d2

        assert copy.copy(d1) == d2
        assert copy.deepcopy(d1) == d2

        d3 = dictobj(a=1, b="2", c=['a', 'b'], d=object())
        d4 = d3.copy()
        assert d4.c is d3.c
        assert d4.d is d3.d
        d4 = copy.copy(d3)
        assert d4.c is d3.c
        assert d4.d is d3.d
        d4 = copy.deepcopy(d3)
        assert d4.c is not d3.c
        assert d4.d is not d3.d


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
        orig = {'a': 'a'}
        d = SimpleMultiDict(orig)
        self.assertEqual(
            repr(d),
            "SimpleMultiDict(%s)" % repr(orig))


if __name__ == '__main__':
    unittest.main()


#EOF
