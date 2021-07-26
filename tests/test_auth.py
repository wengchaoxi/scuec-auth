# -*- coding: utf-8 -*-
import unittest
from scuec_auth.auth import SCUECAuth

class TestAuth(unittest.TestCase):
    def test_login(self):
        uname = ''
        passwd = ''
        sa = SCUECAuth(is_debug=True)
        session = sa.login(uname, passwd, is_verify=False)
        if sa.is_session_valid(session):
            print('login success')
        else:
            print('login failed')

if __name__ == '__main__':
    unittest.main()
