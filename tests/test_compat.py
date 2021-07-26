# -*- coding: utf-8 -*-
import unittest
from scuec_auth._compat import compat_str, compat_bytes

class TestCompat(unittest.TestCase):
    def test_compat(self):
        tmp = '你好世界'
        s = compat_str(tmp)
        print(s)
        s = compat_bytes(tmp)
        print(s)

if __name__ == '__main__':
    unittest.main()