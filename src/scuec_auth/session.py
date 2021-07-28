# -*- coding: utf-8 -*-
"""
    scuec_auth.session
    ~ ~ ~ ~ ~ ~

    :copyright: (c) 2021 by WengChaoxi.
    :license: MIT, see LICENSE for more details.
"""
from time import time as current_time
from requests import Session as SessionBase

class Session(SessionBase):
    def __init__(self):
        super(Session, self).__init__()
        self.last_time = current_time()

    def get(self, url, **kwargs):
        self.last_time = current_time()
        return super(Session, self).get(url, **kwargs)
    
    def head(self, url, **kwargs):
        self.last_time = current_time()
        return super(Session, self).head(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        self.last_time = current_time()
        return super(Session, self).post(url, data=data, json=json, **kwargs)

class SessionCache(object):
    def __init__(self, max_age=1800):
        self.max_age = max_age

        self.__cache_count = 0
        self.__hash_max_size = 0x1C
        self.__cache_hash_table = list()
        for _ in range(self.__hash_max_size):
            self.__cache_hash_table.append(dict())

    def __str__(self):
        cache_table = []
        for t in self.__cache_hash_table:
            if t:
                cache_table.append(t)
        return '[SessionCache] cache_count: %d  cache_max_age: %d  cache_table: %s' %(self.__cache_count, self.max_age, cache_table)

    @staticmethod
    def __hash(data):
        try:
            d1 = ord(data[-1])
            d2 = ord(data[-2])
            d3 = ord(data[-3])
            return (d1+d2+d3-0x90) % 0x1C
        except:
            return len(data) % 0x1C

    def __get(self, username):
        h = self.__hash(username)
        return self.__cache_hash_table[h].get(username)

    def add(self, username, session):
        if session and isinstance(session, Session):
            if not self.__get(username):
                self.__cache_count += 1
            session.last_time = current_time()
            h = self.__hash(username)
            self.__cache_hash_table[h][username] = session
            return True
        return False

    def remove(self, username):
        h = self.__hash(username)
        session = self.__cache_hash_table[h].get(username)
        if session:
            self.__cache_count -= 1
            del self.__cache_hash_table[h][username]
            return True
        return False

    def get_session(self, username):
        session = self.__get(username)
        if session:
            if session.last_time + self.max_age > current_time():
                return session
        return None
    
    def length(self):
        return self.__cache_count
