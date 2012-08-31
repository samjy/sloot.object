#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
import obj_utils


class TestMyobject(unittest.TestCase):
    """Testing myobject
    """

    def test_init(self):
        """Testing initialisation
        """
        o = obj_utils.myobject(test1="test1", test2="test2")
        self.assertEqual(o.test1, "test1")
        self.assertEqual(o.test2, "test2")


if __name__ == '__main__':
    unittest.main()


#EOF
