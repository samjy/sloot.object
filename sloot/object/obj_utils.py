#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from collections.abc import MutableMapping, Mapping
except ImportError:
    from collections import MutableMapping, Mapping


_not_given = object()


class myobject(object):
    """Initialize object attributes using kwargs
    """

    def __init__(self, *args, **kwargs):
        """Initialize
        """
        for k, v in list(kwargs.items()):
            setattr(self, k, v)


class dictobj(dict):
    """Dictionary exposing its values over attributes
    """

    def __init__(self, *args, **kwargs):
        """Initializing

        Works like :py:class:`dict`'s initialization
        """
        for arg in args + (kwargs,):
            dic = arg
            if not isinstance(arg, Mapping):
                dic = dict(arg)

            for k, v in list(dic.items()):
                if isinstance(v, Mapping):
                    v = dictobj(v)

                self[k] = v

        self._initialized = True

    def __repr__(self):
        """Representing dictobj
        """
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def copy(self):
        """Copy the dictobj
        """
        return self.__class__(dict.copy(self))

    def __getattribute__(self, name):
        """Get attribute

        - if it's on the object/class, we'll get it from there
        - otherwise, try to get it from the dict

        NOTE: the object/class attributes take precedence over the dict

        :returns: The attribute
        :raises: (AttributeError) If not there
        """
        dct = dict.__getattribute__(self, '__dict__')
        cls = dict.__getattribute__(self, '__class__')
        if name in dct or hasattr(cls, name) or '_initialized' not in dct:
            # try to get the standard attribute (method, variable, etc) if it's
            # present on the class or we're not initialized
            return dict.__getattribute__(self, name)
        else:
            # when trying to get an unknown attribute, get it from the dict
            try:
                return self.__getitem__(name)
            except Exception:
                # we didn't find the attribute
                pass

        raise AttributeError("%s not found in %s" % (name, cls.__name__))

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised

        NOTE: to avoid issues, we don't allow to setattr on class attributes
            (e.g. to avoid modifying dict.items function)
        """
        try:
            if '_initialized' not in self.__dict__:
                # this test allows attributes to be set in the __init__ method
                return dict.__setattr__(self, item, value)
            elif item in self.__dict__:
                # any normal attributes are handled normally
                return dict.__setattr__(self, item, value)
            elif isinstance(getattr(self.__class__, item, None), property):
                # this allows properties to behave properly
                return dict.__setattr__(self, item, value)
        except AttributeError:
            raise AttributeError(u"Can't set attribute '%s' of %r" % (
                item, self))

        return self.__setitem__(item, value)

    def __delattr__(self, name):
        """Delete attribute
        """
        if name in self.__dict__ or hasattr(self.__class__, name):
            # any normal attributes are handled normally
            return dict.__delattr__(self, name)

        return self.__delitem__(name)


class SimpleMultiDict(dict):
    """Multi dict (a key can have multiple values)
    """

    def getlist(self, key):
        return self[key] if type(self[key]) == list else [self[key]]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'


#EOF
