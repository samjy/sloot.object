#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from setuptools import setup, find_packages
from sloot.object import __VERSION__

setup(
    name="sloot.object",
    version=__VERSION__,
    packages=find_packages(),
    namespace_packages=['sloot',],
    install_requires=[],
    include_package_data=True,
    package_data={'': ['doc/*.rst'],},
    platforms='any',
    test_suite=None,
    author="Samuel Jaillet",
    author_email="sam+dev@samjy.com",
    description="Object utils to make life easier",
    license="MIT",
    keywords=['tools', 'object', 'utils', 'dict'],
    url="https://github.com/samjy/sloot.object",
    download_url="https://github.com/samjy/sloot.object/tarball/%s" % __VERSION__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Freely Distributable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
    ],
)

#EOF
