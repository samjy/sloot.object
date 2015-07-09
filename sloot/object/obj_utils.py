#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

class myobject(object):
    """
    """

    def __init__(self, *args, **kwargs):
        """
        """
        for k, v in kwargs.items():
            setattr(self, k, v)


class dictobj(dict):
    """Dictionary exposing its values over properties
    """

    def __init__(self, *args, **kwargs):
        """Initializing
        """
        self._changed_values = {}
        self._initialized = True

        dicts = []
        for arg in args:
            if not isinstance(arg, dict):
                arg = dict(arg)
            dicts.append(arg)

        dicts.append(kwargs)
        for dic in dicts:
            for k, v in dic.items():
                if isinstance(v, dict):
                    v = dictobj(v)
                self[k] = v

    def __setitem__(self, key, value):
        """Setting items the dict way...
        """
        self._changed_values[key] = value
        super(dictobj, self).__setitem__(key, value)

    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError("%s not found in %s" % (item, self.__class__.__name__))

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        if not self.__dict__.has_key('_initialized'):
            # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif self.__dict__.has_key(item):
            # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)


class SimpleMultiDict(dict):
    """Multi dict (a key can have multiple values)
    """

    def getlist(self, key):
        return self[key] if type(self[key]) == list else [self[key]]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'


#EOF
