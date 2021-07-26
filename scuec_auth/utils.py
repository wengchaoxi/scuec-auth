# -*- coding: utf-8 -*-
"""
    scuec_auth.utils
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
from time import time
from requests import Session as SessionBase
from random import randint
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def debug(tag='debug', msg=None, is_debug=True):
    if is_debug:
        print('[%s] %s'%(tag, msg))

def random_string(size=16)->str:
    aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    aes_chars_len = len(aes_chars)
    string = ''
    for i in range(size):
        string += aes_chars[randint(0, aes_chars_len-1)]
    return string

def encrypt_aes(data, key)->str:
    if isinstance(data, str):
        data = data.encode()
    if isinstance(key, str):
        key = key.encode()
    iv = random_string(AES.block_size).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data, AES.block_size, style='pkcs7'))
    return b64encode(data).decode()

def decrypt_aes(data, key)->str:
    if isinstance(data, str):
        data = b64decode(data.encode())
    if isinstance(key, str):
        key = key.encode()
    iv = random_string(AES.block_size).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(data), AES.block_size, style='pkcs7')
    return data.decode()

def current_timestamp():
    return int(time())

def hash(data):
    d1 = ord(data[-1])
    d2 = ord(data[-2])
    return d1 + d2 - 0x60

class Session(SessionBase):
    def __init__(self, id, max_age=60):
        super().__init__()
        self.sid = hash(id)
        self.max_age = max_age
        self.last_time = current_timestamp()

# TODO
class SessionCache():
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