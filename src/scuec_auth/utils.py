# -*- coding: utf-8 -*-
"""
    scuec_auth.utils
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import print_function

from time import time
from random import randint
from base64 import b64encode, b64decode
from requests import Session as SessionBase
from ._compat import compat_str, compat_bytes, AES, pad, unpad

def debug(tag='null', msg=None, is_debug=True):
    if is_debug:
        print('[debug] tag: %s  msg: %s'%(tag, msg))

def random_string(size=16):
    aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    aes_chars_len = len(aes_chars)
    string = ''
    for i in range(size):
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

def current_timestamp():
    return int(time())

def hash(data):
    d1 = ord(data[-1])
    d2 = ord(data[-2])
    return d1 + d2 - 0x60

class Session(SessionBase):
    def __init__(self, id, max_age=60):
        super(Session, self).__init__()
        self.sid = hash(id)
        self.max_age = max_age
        self.last_time = current_timestamp()

# TODO
class SessionPool(object):
    def __init__(self):
        self.hash_table = []
        for i in range(19):
            self.hash_table.append([])

    def add(self, session):
        pass

    def remove(self, session_id):
        pass

    def get(self, session_id):
        pass