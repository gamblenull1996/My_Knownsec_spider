# -*- coding:utf-8 -*-

"""
v1 spider.py -u url -d deep
v2 spider.py -u url -d deep -f logfile -L loglevel(1-5) --testself
v3 -thread number
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from database import DataStore
from args_parser import get_args


def get_hyper_links(url, url_list, keyword, depth, db):
    # url去重
    if url not in url_list:
        data = get_html(url)
        if data is not None:
            soup = BeautifulSoup(data, 'lxml')
            # 提取页面中的超链接
            a_tags = soup.find_all("a", attrs={"href": re.compile("^http://")})
            # 将url链接, keyword关键字，html文档插入sqlite3
            if keyword == "":
                db.insert(url, str(None), data)
                print "insert {} to database".format(url)
            else:
                if keyword in data:
                    db.insert(url, keyword, data)
                    print "insert {} with {} to database".format(url, keyword)
            # 遍历页面中的a标签
            for i in a_tags:
                if 'href' in i.attrs and i["href"] not in url_list:
                    url_list.append(i["href"])
                    # 通过递归找到每层的所有url
                    if depth > 0:
                        get_hyper_links(
                            i["href"], url_list, keyword, depth - 1, db)


def get_html(url):
    # 设置爬虫UA
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        # requests完成编码处理
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text
        return html
    except BaseException:
        return None


def spider(args, db):
    # 用于存放所有的url
    url_list = []
    start_url = args.url
    depth = args.depth
    keyword = args.keyword
    get_hyper_links(start_url, url_list, keyword, depth, db)


if __name__ == '__main__':
    start = time.time()
    args = get_args()
    db = DataStore(args.dbfile)
    spider(args, db)
    db.close()
    end = time.time()
    print "time cost: {}s".format(end - start)
