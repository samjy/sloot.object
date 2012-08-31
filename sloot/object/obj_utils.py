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


#EOF
