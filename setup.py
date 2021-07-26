# -*- coding: utf-8 -*-
"""
    scuec_auth
    ~ ~ ~ ~ ~ ~
    The authentication module of SCUEC.

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
from os import  path
from codecs import open
from setuptools import setup, find_packages

basedir = path.abspath(path.dirname(__file__))

with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'SCUECAuth', 
    version = '1.0.0',
    url = 'https://github.com/WengChaoxi/scuec-auth',
    author = 'WengChaoxi',
    author_email = '352120190@qq.com',

    description = 'The authentication module of SCUEC.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    license = 'MIT',
    platforms = 'any',
    
    packages = find_packages(where='src'),
    include_package_data = True,
    zip_safe = False,

    python_requires='>=3.5, <4',
    install_requires = [
        'requests',
        'bs4',
        'pycryptodome'
    ],
    extras_require = {
        'PyExecJS': ['PyExecJS']
    },
    keywords = 'scuec, auth',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only'
    ]
)