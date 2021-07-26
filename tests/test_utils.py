# -*- coding: utf-8 -*-
import unittest
from scuec_auth.utils import random_string, encrypt_aes, decrypt_aes

class TestUitls(unittest.TestCase):
    def test_encrypt(self):
        s = random_string(64)+'hello world'
        k = random_string(16)
        d = encrypt_aes(s, k)
        print(d)
        s_ = decrypt_aes(d, k)[64:]
        print(s_)

if __name__ == '__main__':
    unittest.main()