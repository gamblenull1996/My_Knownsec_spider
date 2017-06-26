# -*- coding:utf-8 -*-

import time
import logging
import requests
import traceback
from urlparse import urljoin
from bs4 import BeautifulSoup
from database import DataStore
from args_parser import get_args
from log_setting import logging_config
from my_threadpool import MyThreadPool

log = logging.getLogger('spider')


class Spider(object):
    def __init__(self, args):
        self.url = args.url
        self.depth = args.depth
        self.dbfile = args.dbfile
        self.logfile = args.logfile
        self.keyword = args.keyword
        self.thread_num = args.thread_num

        self.url_set = set()
        self.threadpool = MyThreadPool(self.thread_num)

    def start(self):
        self.threadpool.add_task(self.get_and_store, self.url, self.depth)
        self.threadpool.wait_completion()

    def get_and_store(self, url, depth):
        if url in self.url_set:
            log.debug("{} has been crawled".format(url))
            return
        else:
            self.url_set.add(url)
            log.debug("add {} to url_set".format(url))

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/57.0.2987.110 Safari/537.36",
        }
        try:
            log.warning("get {}".format(url))
            r = requests.get(url, headers=headers, timeout=10)
            r.encoding = r.apparent_encoding
            r.raise_for_status()
            html = r.content
        except Exception as e:
            log.critical(
                "Failed to get {} depth:{} error:{}".format(
                    url, depth, e), exc_info=True)
            return

        soup = BeautifulSoup(html, 'lxml')
        db = DataStore(self.dbfile)

        if self.keyword == "":
            db.insert(url, str(None), html)
            db.close()
        else:
            db.insert(url, self.keyword, html)
            db.close()

        self.get_hyperlink(url, soup, depth - 1)

    def get_hyperlink(self, url, soup, depth):
        if depth > 0:
            for link in soup.find_all('a'):
                new = link.get('href').rstrip('/')
                # 使用urljoin对相对链接做处理
                if not new.startswith("http"):
                    new = urljoin(url, new)
                self.threadpool.add_task(self.get_and_store, new, depth)

    def get_url_set(self):
        return self.url_set


if __name__ == '__main__':
    start = time.time()
    args = get_args()
    logging_config(log, args.logfile, args.loglevel)
    spider = Spider(args)
    spider.start()
    end = time.time()
    # print spider.get_url_set()
    print "time cost: {}s".format(end - start)
