# -*- coding:utf-8 -*-
import sys
import time
import logging
import threading
import requests
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
        # 建立起线程池，添加任务，等待所有任务结束
        self.threadpool.add_task(self.get_and_store, self.url, self.depth)

    def wait(self):
        self.threadpool.wait_completion()

    def get_and_store(self, url, depth):
        """
        根据给定的url获取并存储html页面
        :param url: 要被下载的url链接
        :param depth: url链接的深度
        """
        # url去重
        if url in self.url_set:
            log.debug("{} has been crawled".format(url))
            return
        else:
            self.url_set.add(url)
            log.debug("add {} to url_set".format(url))
        # 为爬虫添加headers
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
            # 处理编码
            r.encoding = r.apparent_encoding
            r.raise_for_status()
            html = r.content
        except Exception as e:
            log.critical(
                "Failed to get {} depth:{} error:{}".format
                (url, depth, e),
                exc_info=True
            )
            return

        # 解析HTML
        soup = BeautifulSoup(html, 'lxml')
        # 连接数据库
        db = DataStore(self.dbfile)

        if self.keyword == "":
            db.insert(url, str(None), html)
            db.close()
        else:
            if self.keyword in html:
                db.insert(url, self.keyword, html)
                db.close()
            else:
                log.warning("Cannot find {} in {}".format(self.keyword, url))
        # 获取该页面内的链接，深度减一
        self.get_hyperlink(url, soup, depth - 1)

    def get_hyperlink(self, url, soup, depth):
        """
        获得该url页面所有的链接
        :param url: 要被提取链接的url
        :param soup: url对应的HTML解析器
        :param depth: url的深度
        """
        if depth > 0:
            for link in soup.find_all('a'):
                new = link.get('href').rstrip('/')
                # 使用urljoin对相对链接做处理
                if not new.startswith("http"):
                    new = urljoin(url, new)
                self.threadpool.add_task(self.get_and_store, new, depth)

    def get_url_set_size(self):
        return len(self.url_set)


class PrintToCommand(threading.Thread):
    """
    每隔10秒在命令行打印一次状态信息
    """
    def __init__(self, spider, threadpool):
        threading.Thread.__init__(self)
        self.threadpool = threadpool
        self.spider = spider
        self.daemon = True
        self.start()

    def run(self):
        while True:
            already = self.spider.get_url_set_size()
            remain = self.threadpool.get_size()
            if remain == 0 and already > remain:
                # 打印出最后一次的队列状态，然后跳出循环
                print "{} tasks in the ThreadPool, already visted: {} \n".format(remain, already)
                break
            else:
                log.warning("print crawling status to command line")
                print "{} tasks in the ThreadPool, already visted: {} \n".format(remain, already)
                time.sleep(10)


if __name__ == '__main__':
    start = time.time()
    args = get_args()
    logging_config(log, args.logfile, args.loglevel)
    try:
        spider = Spider(args)
        print_process = PrintToCommand(spider, spider.threadpool)
        spider.start()
        print_process.run()
        spider.wait()
    except KeyboardInterrupt:
        print "exiting from spider"
        log.error("canceled by user")
        sys.exit()
    end = time.time()
    print "time cost: {}s".format(end - start)
