# -*- coding:utf-8 -*-
import sqlite3
import logging

log = logging.getLogger('spider.database')


class DataStore(object):
    def __init__(self, dbfile):
        self.dbfile = dbfile
        try:
            log.warning("open database: {}".format(dbfile))
            # 连接数据库，如果数据库不存在，就创建一个
            self.conn = sqlite3.connect(dbfile)
            # 设置成unicode以支持中文
            self.conn.text_factory = str
        except sqlite3.Error as e:
            log.error("Failed to connect:{} {}".format(dbfile, e))
            return

        self.cur = self.conn.cursor()

        try:
            # 数据库表结构为url+keyword+html
            self.cur.execute('''
                create table if not exists data(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url text,
                    keyword text,
                    html text
                )
            ''')
        except sqlite3.Error as e:
            log.error("Failed to create:{} {}".format(dbfile, e))
            # 出错就回滚
            self.conn.rollback()

        self.conn.commit()

    def insert(self, url, keyword, html):
        try:
            log.warning("insert {} to database {}".format(url, self.dbfile))
            self.cur.execute(
                "insert into data (url, keyword, html) values (?,?,?)",
                (url, keyword, html))
        except sqlite3.Error as e:
            log.error("Failed to insert {} to database {}".format(url, e))
            # 出错就回滚
            self.conn.rollback()

        self.conn.commit()

    def close(self):
        log.info("close database")
        self.cur.close()
        self.conn.close()
