# -*- coding: utf-8 -*-
"""
    scuec_auth.auth
    ~ ~ ~ ~ ~ ~
    The authentication module of SCUEC.

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
import re
from bs4 import BeautifulSoup
from bs4.element import Tag as bs4_element_tag
from .utils import Session, debug, random_string, encrypt_aes

simple_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

# def encrypt_aes_by_js(self, data, key)->str:
#     url_encryptjs = 'https://id.scuec.edu.cn/authserver/default/static/common/encrypt.js'
#     try:
#         import os
#         import execjs
#         os.environ['EXECJS_RUNTIME'] = 'JScript'
#         js = requests.get(url=url_encryptjs, headers=simple_headers).text
#         ctx = execjs.compile(js)
#         data = ctx.call('encryptAES', data, key)
#     except:
#         debug('encrypt by js', 'get encrypt.js error')
#     return data

def encrypt_passwd(passwd, salt)->str:
    # return encrypt_aes_by_js(passwd, salt)
    return encrypt_aes(random_string(64)+passwd, salt)

def is_username_valid(username):
    if len(username)==0:
        return False
    pattern_tno = r'^\d{7}$'
    pattern_sno = r'^\d{12}$'
    t_r = re.match(pattern_tno, username)
    s_r = re.match(pattern_sno, username)
    if t_r or s_r:
        return True
    return False

class SCUECAuth():
    def __init__(self, is_verify=True, is_debug=False):
        self.uname = ''
        self.passwd = ''
        self.is_verify = is_verify
        self.is_debug = is_debug
        self.session = None

    def __verify(self, session)->bool:
        try:
            data = session.get('https://id.scuec.edu.cn/personalInfo/personCenter/index.html#/accountsecurity', headers=simple_headers)
            data.encoding = data.apparent_encoding
            data = data.text
        except:
            debug('verify', 'get index.html error', self.is_debug)
            return False
        soup = BeautifulSoup(data, 'html.parser')
        if soup and soup.title.text=="个人中心":
            debug('verify', 'login succes', self.is_debug)
            return True
        debug('verify', 'login failed', self.is_debug)
        return False

    def __build_session(self)->Session:
        self.session = None
        session = Session(self.uname)
        url_login = 'https://id.scuec.edu.cn/authserver/login'
        try:
            data = session.get(url=url_login, headers=simple_headers).text
        except:
            debug('build session', 'get login.html error', self.is_debug)
            return None
        soup = BeautifulSoup(data, 'html.parser')
        tmp_salt = soup.find('input', {'type':'hidden', 'id':'pwdEncryptSalt'})
        tmp_exec = soup.find('input', {'type':'hidden', 'name':'execution'})
        if isinstance(tmp_salt, bs4_element_tag) and isinstance(tmp_exec, bs4_element_tag):
            salt = tmp_salt.attrs.get('value')
            exec_ = tmp_exec.attrs.get('value')
            if not (salt and exec_):
                return None
            passwd = encrypt_passwd(self.passwd, salt)
            data = {
                'username': self.uname,
                'password': passwd,
                'captcha': '',
                '_eventId': 'submit',
                'cllt': 'userNameLogin',
                'lt': '',
                'execution': exec_
            }
            try:
                session.post(url=url_login, data=data, headers=simple_headers)
            except:
                debug('build session', 'post user data failed', self.is_debug)
                return None
            if self.is_verify:
                if self.__verify(session):
                    self.session = session
                else:
                    self.session = None
            else:
                self.session = session
            return self.session

    def login(self, username, password, is_verify=True)->Session:
        if not is_username_valid(username):
            return None
        self.uname = username
        self.passwd = password
        self.is_verify = is_verify
        return self.__build_session()
    
    def is_session_valid(self, session)->bool:
        return self.__verify(session)

    def logout(self):
        pass
