# -*- coding:utf-8 -*-
import sqlite3


class DataStore(object):
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        # 数据库表结构为url+keyword+html
        self.cur.execute('''
            create table if not exists data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url text,
                keyword text,
                html text
            )
        ''')
        self.conn.commit()

    def insert(self, url, keyword, html):
        self.cur.execute(
            "insert into data (url, keyword, html) values (?,?,?)",
                (url, keyword, html))
        self.conn.commit()

    def close(self):
        self.conn.close()
