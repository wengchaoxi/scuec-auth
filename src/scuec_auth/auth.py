# -*- coding: utf-8 -*-
"""
    scuec_auth.auth
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
import re
from bs4 import BeautifulSoup
from bs4.element import Tag as bs4_element_tag
from ._compat import compat_str
from .utils import debug, random_string, encrypt_aes
from .session import Session, SessionCache

simple_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

class SCUECAuth(object):
    def __init__(self, is_verify=True, is_debug=False):
        self.is_verify = is_verify
        self.is_debug = is_debug

        self.__uname = ''
        self.__passwd = ''
        self.__session = None
        self.__session_cache = None

    def __str__(self):
        max_age = 0
        if self.__session_cache:
            max_age = self.__session_cache.max_age
        return '[SCUECAuth] is_verify: %s  session_cache_max_age: %s  is_debug: %s' \
            % (self.is_verify, max_age, self.is_debug)

    def __build_session(self, username, password):
        session = Session()
        url_login = 'http://id.scuec.edu.cn/authserver/login'
        try:
            data = session.get(url=url_login, headers=simple_headers).text
        except:
            debug('SCUECAuth.__build_session', 'get login.html error', self.is_debug)
            return None
        soup = BeautifulSoup(data, 'html.parser')
        tmp_salt = soup.find('input', {'type':'hidden', 'id':'pwdEncryptSalt'})
        tmp_exec = soup.find('input', {'type':'hidden', 'name':'execution'})
        if not isinstance(tmp_salt, bs4_element_tag) or not isinstance(tmp_exec, bs4_element_tag):
            return None
        salt = tmp_salt.attrs.get('value')
        exec_ = tmp_exec.attrs.get('value')
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
            debug('SCUECAuth.__build_session', 'post login data error', self.is_debug)
            return None
        return session

    def __verify(self, session):
        try:
            data = session.get('http://id.scuec.edu.cn/personalInfo/personCenter/index.html#/accountsecurity', headers=simple_headers)
            data.encoding = data.apparent_encoding
            data = data.text
        except:
            debug('SCUECAuth.__verify', 'get index.html error', self.is_debug)
            return False
        soup = BeautifulSoup(data, 'html.parser')
        if soup and compat_str(soup.title.text)=="个人中心":
            return True
        return False

    def __login(self, username, password):
        self.__uname = username
        self.__passwd = password
        session = None
        if self.__session_cache:
            session = self.__session_cache.get_session(self.__uname)
            if session is None:
                session = self.__build_session(self.__uname, self.__passwd)
                if self.__verify(session):
                    self.__session_cache.add(self.__uname, session)
            self.__session = session
        else:
            session = self.__build_session(self.__uname, self.__passwd)
            if self.is_verify and not self.__verify(session):
                session.close()
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
        if not self.is_username_valid(username):
            return None
        return self.__login(username, password)
    
    def verify_session(self, session):
        if session is None or not isinstance(session, Session):
            return False
        return self.__verify(session)

    def logout(self, username=''):
        session = self.__session
        if username != '':
            if self.__session_cache:
                session = self.__session_cache.get_session(username)
        if session is None:
            return False
        url_logout = 'http://id.scuec.edu.cn/authserver/logout'
        try:
            session.get(url=url_logout, headers=simple_headers)
            session.close()
        except:
            debug('SCUECAuth.logout', 'get logout.html error', self.is_debug)
            return False
        if self.__session_cache:
            self.__session_cache.remove(username)
        self.__session = None
        return True

    def open_session_cache(self, max_age=1800):
        if max_age <= 0:
            debug('SCUECAuth.open_session_cache', 'max_age must >0', self.is_debug)
            return False
        if self.__session_cache:
            self.__session_cache.max_age = max_age
        else:
            self.__session_cache = SessionCache(max_age)
        return True
    
    def close_session_cache(self):
        if self.__session_cache:
            del self.__session_cache
            self.__session_cache = None
            return True
        return False
