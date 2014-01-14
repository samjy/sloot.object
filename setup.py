#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from setuptools import setup, find_packages

setup(
    name="sloot.object",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['sloot',],
    install_requires=['nose', 'coverage'],
    include_package_data=True,
    package_data={'': ['doc/*.rst'],},
    platforms='any',
    test_suite=None,
    author="Samuel Jaillet",
    author_email="sam+dev@samjy.com",
    description="object utils",
    license="MIT?",
    keywords="tools object utils",
    url="http://samjy.com",
)

#EOF
