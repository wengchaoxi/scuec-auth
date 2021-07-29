# -*- coding: utf-8 -*-
"""
    scuec_auth.utils
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import print_function

from random import randint
from base64 import b64encode, b64decode
from functools import wraps
from ._compat import compat_str, compat_bytes, AES, pad, unpad, clock_cpu, clock

def debug(tag='', msg=None, is_debug=True):
    if is_debug:
        print('[debug] tag: %s  msg: %s'%(tag, msg))

def random_string(size=16):
    aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    aes_chars_len = len(aes_chars)
    string = ''
    for _ in range(size):
        string += aes_chars[randint(0, aes_chars_len-1)]
    return string

def random_bytes(size=16):
    return compat_bytes(random_string(size))

def encrypt_aes(data, key):
    data = compat_bytes(data)
    key = compat_bytes(key)
    iv = random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data, AES.block_size, style='pkcs7'))
    return compat_str(b64encode(data))

def decrypt_aes(data, key):
    data = b64decode(compat_bytes(data))
    key = compat_bytes(key)
    iv = random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(data), AES.block_size, style='pkcs7')
    return compat_str(data)

def time_counter(just_cpu=False):
    def inner(func):
        c = clock_cpu if just_cpu else clock
        @wraps(func)
        def wrapper(*args, **kwargs):
            begin = c()
            r = func(*args, **kwargs)
            end = c()
            print('[time_counter.{}] {:.3f}s'.format(func.__name__, end-begin))
            return r
        return wrapper
    return inner
