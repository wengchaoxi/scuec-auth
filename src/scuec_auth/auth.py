# -*- coding: utf-8 -*-
"""
    scuec_auth.auth
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
import re
from ._compat import compat_str, string_types
from .utils import error, debug, random_string, encrypt_aes
from .session import Session, SessionCache

simple_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

class SCUECAuth(object):
    def __init__(self, is_verify=True, is_debug=False):
        self.is_verify = is_verify
        self.is_debug = is_debug

        self.__regex_login = re.compile(r'<input type="hidden" id="pwdEncryptSalt" value="(.*)" /><input type="hidden" id="execution" name="execution" value="(.*)" />')
        self.__regex_verify = re.compile(r'<title>(.*)</title>')
        self.__session = None
        self.__session_cache = None

    def __del__(self):
        if self.__session:
            del self.__session
        if self.__session_cache:
            del self.__session_cache

    def __str__(self):
        max_age = 0
        if self.__session_cache:
            max_age = self.__session_cache.max_age
        return '[SCUECAuth] is_verify: %s  session_cache_max_age: %s  is_debug: %s' \
            % (self.is_verify, max_age, self.is_debug)

    def __build_session(self, username, password):
        session = Session(username, password)
        url_login = 'http://id.scuec.edu.cn/authserver/login'
        try:
            data = session.get(url=url_login, headers=simple_headers).text
        except:
            error('SCUECAuth.__build_session', 'get login.html error')
            return None

        # from bs4 import BeautifulSoup
        # from bs4.element import Tag
        #
        # soup = BeautifulSoup(data, 'html.parser')
        # tmp_salt = soup.find('input', {'type':'hidden', 'id':'pwdEncryptSalt'})
        # tmp_exec = soup.find('input', {'type':'hidden', 'name':'execution'})
        # if not isinstance(tmp_salt, Tag) or not isinstance(tmp_exec, Tag):
        #     return None
        # salt = tmp_salt.attrs.get('value')
        # exec_ = tmp_exec.attrs.get('value')
        m = self.__regex_login.search(data)
        if m is None:
            return None
        salt = m.group(1)
        exec_ = m.group(2)

        if salt is None or exec_ is None:
            return None
        data = {
            'username': username,
            'password': encrypt_aes(random_string(64)+password, salt),
            'captcha': '',
            '_eventId': 'submit',
            'cllt': 'userNameLogin',
            'lt': '',
            'execution': exec_
        }
        try:
            session.post(url=url_login, data=data, headers=simple_headers)
        except:
            error('SCUECAuth.__build_session', 'post login data error')
            return None
        return session

    def __verify(self, session):
        try:
            data = session.get('http://id.scuec.edu.cn/personalInfo/personCenter/index.html#/accountsecurity', headers=simple_headers)
            data.encoding = data.apparent_encoding
            data = data.text
        except:
            error('SCUECAuth.__verify', 'get index.html error')
            return False

        # from bs4 import BeautifulSoup
        #
        # soup = BeautifulSoup(data, 'html.parser')
        # if soup and compat_str(soup.title.text)=="个人中心":
        #     return True
        m = self.__regex_verify.search(data)
        if m and compat_str(m.group(1)) == "个人中心":
            return True

        return False

    def __login(self, username, password):
        session = None
        if self.__session_cache:
            session = self.__session_cache.get_session(username)
            if session and session.passwd!=password:
                session = None
            if session is None:
                session = self.__build_session(username, password)
                if session:
                    if self.__verify(session):
                        self.__session_cache.add(username, session)
                    else:
                        session = None
            self.__session = session
        else:
            session = self.__build_session(username, password)
            if session and self.is_verify and not self.__verify(session):
                session = None
            self.__session = session
        return self.__session

    @staticmethod
    def is_username_valid(username):
        if len(username)==0:
            return False
        t = re.match(r'^\d{7}$', username)
        s = re.match(r'^\d{12}$', username)
        if t or s:
            return True
        return False

    def login(self, username, password):
        if not isinstance(username, string_types) or not isinstance(password, string_types):
            error('SCUECAuth.login', 'username and password must be string type')
            return None
        if not self.is_username_valid(username):
            error('SCUECAuth.login', 'username is invalid')
            return None
        session = self.__login(username, password)
        if session:
            msg = '' if self.is_verify or self.__session_cache else ', but session is not verified'
            debug('SCUECAuth.login', 'login success%s'%msg, self.is_debug)
        else:
            debug('SCUECAuth.login', 'login failed', self.is_debug)
        return session
    
    def verify_session(self, session):
        if session is None or not isinstance(session, Session):
            return False
        return self.__verify(session)

    def logout(self, username=''):
        if not isinstance(username, string_types):
            return False
        session = self.__session
        if username:
            if not self.is_username_valid(username):
                error('SCUECAuth.logout', 'username is invalid')
                return False
            session = self.__session_cache.get_session(username) if self.__session_cache else None
        if session is None:
            return False
        url_logout = 'http://id.scuec.edu.cn/authserver/logout'
        try:
            session.get(url=url_logout, headers=simple_headers)
        except:
            error('SCUECAuth.logout', 'get logout.html error')
            return False
        if self.__session_cache:
            self.__session_cache.remove(username)
        else:
            del self.__session
            self.__session = None
        debug('SCUECAuth.logout', 'logout success', self.is_debug)
        return True

    def open_session_cache(self, max_age=1800):
        if max_age <= 0:
            error('SCUECAuth.open_session_cache', 'max_age must >0')
            return False
        if self.__session_cache:
            self.__session_cache.max_age = max_age
        else:
            self.__session_cache = SessionCache(max_age)
            debug('SCUECAuth.open_session_cache', 'session cache has opened', self.is_debug)
        return True
    
    def close_session_cache(self):
        if self.__session_cache:
            del self.__session_cache
            self.__session_cache = None
            debug('SCUECAuth.close_session_cache', 'session cache has closed', self.is_debug)
            return True
        debug('SCUECAuth.close_session_cache', "session cache not open", self.is_debug)
        return False
