import unittest
from scuec_auth import SCUECAuth

class TestSimple(unittest.TestCase):
    def test_login(self):
        uname = ''
        passwd = ''
        sa = SCUECAuth(is_debug=True)
        sa.login(uname, passwd, False)
        if sa.is_session_valid(sa.session):
            print('success')
        else:
            print('failed')

if __name__ == '__main__':
    unittest.main()
