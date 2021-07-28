# -*- coding: utf-8 -*-
"""
    scuec_auth
    ~ ~ ~ ~ ~ ~
    The authentication module of SCUEC. ( https://github.com/WengChaoxi/scuec-auth )

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
from ._compat import compat_str, compat_bytes
from .utils import debug, random_string, random_bytes, encrypt_aes, decrypt_aes
from .session import Session, SessionCache
from .auth import simple_headers, SCUECAuth

__version__ = '1.0.0'
__all__ = ['compat_str', 'compat_bytes', 'debug', 'random_string', 'random_bytes', 'encrypt_aes', 'decrypt_aes', 'Session', 'SessionCache', 'simple_headers', 'SCUECAuth']
