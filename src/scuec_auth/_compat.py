# -*- coding: utf-8 -*-
"""
    scuec_auth._compat
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
import sys

if sys.version_info[0] == 2:
    def iteritems(d):
        return d.iteritems()

    def iterkeys(d):
        return d.iterkeys()

    def itervalues(d):
        return d.itervalues()

    def compat_str(x, encoding='utf-8', errors='strict'):
        if x is None or isinstance(x, str):
            return x
        if isinstance(x, unicode):
            return x.encode(encoding, errors)
        return str(x)

    def compat_bytes(x, encoding='utf-8', errors='strict'):
        return compat_str(x, encoding, errors)

    string_types = (unicode, str)
else:
    def iteritems(d):
        return iter(d.items())

    def iterkeys(d):
        return iter(d.keys())
    
    def itervalues(d):
        return iter(d.values())

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

    string_types = (str, )

try:
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad, unpad
except ImportError:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad

try:
    from time import process_time as clock_cpu, perf_counter as clock
except ImportError:
    from time import clock as clock_cpu, time as clock
