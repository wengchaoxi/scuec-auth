# -*- coding: utf-8 -*-
import unittest
from scuec_auth.auth import SCUECAuth

class TestAuth(unittest.TestCase):
    def test_login(self):
        uname = ''
        passwd = ''
        sa = SCUECAuth(is_verify=False, is_debug=True)
        sa.open_session_cache(5)
        session = sa.login(uname, passwd)
        if sa.verify_session(session):
            print('login success')
        else:
            print('login failed')
        sa.close_session_cache()

if __name__ == '__main__':
    unittest.main()
