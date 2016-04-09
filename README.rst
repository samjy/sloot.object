***************************
sloot.object - Object tools
***************************


::

  >>> from sloot.object import dictobj
  >>> d = dictobj({'a': 'a', 'b': 'b'}, c='c')
  >>> print d
  dictobj({'a': 'a', 'c': 'c', 'b': 'b'})
  >>> d.a
  'a'
  >>> d.a = 3
  >>> print d
  dictobj({'a': 3, 'c': 'c', 'b': 'b'})
  >>> print dict(d)
  {'a': 3, 'c': 'c', 'b': 'b'}


.. EOF
