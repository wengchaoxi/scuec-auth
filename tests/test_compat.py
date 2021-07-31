# -*- coding: utf-8 -*-
import unittest
from scuec_auth._compat import compat_str, compat_bytes, iterkeys, itervalues, iteritems

class TestCompat(unittest.TestCase):
    def test_compat(self):
        tmp = '你好世界'
        s = compat_str(tmp)
        print(s)
        s = compat_bytes(tmp)
        print(s)

        d = {'1': '111', '2': '222'}
        for k in iterkeys(d):
            print(k)
        for v in itervalues(d):
            print(v) 
        for i in iteritems(d):
            print(i)
        


if __name__ == '__main__':
    unittest.main()