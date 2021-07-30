# -*- coding: utf-8 -*-
import unittest
from scuec_auth.auth import SCUECAuth

sa = SCUECAuth(is_verify=False, is_debug=True)

class TestAuth(unittest.TestCase):
    def test_login(self):
        uname = ''
        passwd_error = ''
        passwd_correct = ''
        
        session = sa.login(uname, passwd_error)
        if sa.verify_session(session):
            print('login success')
        else:
            print('login failed')


        def u(msg=''):
            session = sa.login(uname, passwd_correct)
            print('%s: %s' % (msg, session))

        u('不缓存')
        u('不缓存')
        sa.open_session_cache(2)
        u('使用缓存')
        u('使用缓存')
        u('使用缓存')
        u('使用缓存')
        u('使用缓存')
        u('使用缓存')
        u('使用缓存')
        sa.close_session_cache()
        u('不缓存')

if __name__ == '__main__':
    unittest.main()
