***************************
sloot.object - Object tools
***************************

.. image:: https://travis-ci.org/samjy/sloot.object.svg?branch=master
   :target: https://travis-ci.org/samjy/sloot.object


Basic usage
===========

::

  >>> from sloot.object import dictobj
  >>> d = dictobj({'a': 'a', 'b': 'b'}, c='c')
  >>> print(d)
  dictobj({'a': 'a', 'b': 'b', 'c': 'c'})
  >>> d.a
  'a'
  >>> d['a']
  'a'
  >>> d.a = 3
  >>> d.a
  3
  >>> d['a'] = 42
  >>> d.a
  42
  >>> print(d)
  dictobj({'a': 42, 'c': 'c', 'b': 'b'})
  >>> print(dict(d))
  {'a': 42, 'c': 'c', 'b': 'b'}



Behavior of setattr in inherited objects
========================================

::

  >>> class T(dictobj):
  ...   classvar = 'classvar'
  ...   def f(self):
  ...     return 'f'
  ...   @property
  ...   def prop(self):
  ...     return getattr(self, '_prop', 'prop')
  ...   @prop.setter
  ...   def prop(self, value):
  ...     self._prop = value
  ...


- methods and class attributes are not overwritten and go to the dict::

    >>> t = T({'classvar': 1, 'f': 2, 'prop': 3})
    >>> t.classvar  # access the class attribute
    'classvar'
    >>> t['classvar']  # access the dict entry
    1
    >>> t.classvar = 5  # we don't overwrite class attributes, this goes to dict
    >>> t.classvar  # this is the class attribute
    'classvar'
    >>> t['classvar']
    5
    >>> t.f  # access the class method
    <bound method T.f of T({'classvar': 1, 'f': 2, 'prop': 3})>
    >>> t['f']  # access the dict entry
    2
    >>> t.f = 4  # we don't overwrite the method, this goes to the dict
    >>> t.f
    <bound method T.f of T({'classvar': 1, 'f': 2, 'prop': 3})>
    >>> t['f']
    4

- properties getter and setter are used::

    >>> t.prop  # get the property
    'prop'
    >>> t['prop']  # get the dict entry
    3
    >>> t.prop = 'newprop'  # use property setter
    >>> t.prop
    'newprop'
    >>> t['prop']
    3

- otherwise the dict is updated::

    >>> t.a = 42
    >>> t['a']
    42
    >>> t.a
    42


.. EOF
