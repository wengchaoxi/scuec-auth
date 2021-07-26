# -*- coding: utf-8 -*-
"""
    scuec_auth._compat
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""

import sys

py3 = sys.version_info[0] == 3

if not py3:
    def compat_str(x, encoding='utf-8', errors='strict'):
        if x is None or isinstance(x, str):
            return x
        if isinstance(x, unicode):
            return x.encode(encoding, errors)
        return str(x)

    def compat_bytes(x, encoding='utf-8', errors='strict'):
        return compat_str(x, encoding, errors)
else:
    def compat_str(x, encoding='utf-8', errors='strict'):
        if x is None or isinstance(x, str):
            return x
        if isinstance(x, bytes):
            return x.decode(encoding, errors)
        return str(x)

    def compat_bytes(x, encoding='utf-8', errors='strict'):
        if x is None or isinstance(x, bytes):
            return x
        if isinstance(x, str):
            return x.encode(encoding, errors)
        return bytes(x)

try:
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad, unpad
except ImportError:
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
    except ImportError:
        sys.exit('import error')