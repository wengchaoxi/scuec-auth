# -*- coding: utf-8 -*-
"""
    scuec_auth
    ~ ~ ~ ~ ~ ~
    The authentication module of SCUEC.

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""

from .utils import debug, encrypt_aes, decrypt_aes
from .auth import simple_headers, SCUECAuth

__version__ = '1.0.0'
__all__ = ['debug', 'encrypt_aes', 'decrypt_aes', 'simple_headers', 'SCUECAuth']
