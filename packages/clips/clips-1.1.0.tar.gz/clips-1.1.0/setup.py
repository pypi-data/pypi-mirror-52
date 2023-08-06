#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path as os_path
from setuptools import setup

# Package meta-data.
NAME = 'clips'
DESCRIPTION = 'Parser for command-line applications.'
URL = 'https://github.com/acapitanelli/clips'
AUTHOR = 'Andrea Capitanelli'
EMAIL = 'andrea@capitanelli.gmail.com'
VERSION = '1.1.0'

# short/long description
here = os_path.abspath(os_path.dirname(__file__))
try:
    with open(os_path.join(here, 'README.md'), 'r', encoding='utf-8') as file:
        long_desc = '\n' + file.read()
except FileNotFoundError:
    long_desc = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=NAME,
    maintainer_email=EMAIL,
    url=URL,
    py_modules=['clips'],
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords='cli parser commands arguments colors',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities'
    ],
    test_suite='tests',
)
