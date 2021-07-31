# -*- coding: utf-8 -*-
import unittest
from scuec_auth.auth import SCUECAuth

sa = SCUECAuth(is_verify=True, is_debug=True)
import time

class TestAuth(unittest.TestCase):
    def test_login(self):
        uname = '201821094029'
        passwd_error = 'wcx'
        passwd_correct = 'wcx990122'
        
        session = sa.login(uname, passwd_error)
        if sa.verify_session(session):
            print('login success')
        else:
            print('login failed')

        def u(msg, password):
            session = sa.login(uname, password)
            time.sleep(1)
            if sa.verify_session(session):
                print('yes!!!', end='')
            else:
                print('no!!!', end='')
            sa.logout()
            print('%s: %s' % (msg, session))
        u('不缓存,正确', passwd_correct)
        u('不缓存,正确', passwd_correct)
        sa.open_session_cache(5)
        u('使用缓存,正确', passwd_correct)
        u('使用缓存,正确', passwd_correct)
        u('使用缓存,错误', passwd_error)
        u('使用缓存,正确', passwd_correct)
        sa.close_session_cache()
        u('不缓存，正确', passwd_correct)

if __name__ == '__main__':
    unittest.main()
