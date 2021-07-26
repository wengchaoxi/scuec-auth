# -*- coding: utf-8 -*-
"""
    scuec_auth
    ~ ~ ~ ~ ~ ~
    The authentication module of SCUEC.

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
from setuptools import setup

# Metadata goes in setup.cfg.
setup(
    name = 'SCUECAuth',

    install_requires = [
        'requests',
        'bs4',
        'pycryptodome'
    ],
    extras_require = {}
)