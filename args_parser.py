# -*- coding:utf-8 -*-
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest="url", default="", help=u"起始url")
    parser.add_argument("-d", type=int, dest="depth", default=0, help=u"爬取深度")
    parser.add_argument(
        "--thread",
        type=int,
        dest="thread_num",
        default=10,
        help=u"并发线程数")
    parser.add_argument(
        '--dbfile',
        dest="dbfile",
        default="spider.db",
        help=u"sqlite文件名")
    parser.add_argument(
        '-f',
        dest="logfile",
        default="spider.log",
        help=u"日志文件名")
    parser.add_argument(
        '-l',
        dest="loglevel",
        default="5",
        type=int,
        help=u"日志记录详细程度，数字越大记录越详细(1-5)")
    parser.add_argument(
        '--keyword',
        dest="keyword",
        default="",
        help=u"设置关键词，爬取满足该关键词的网页，默认获取所有页面")
    # parser.add_argument('--encoding', dest="encoding", default=None, help=u"指定页面编码，如果不指定将自动测试页面编码")
    # store_true参数用于保存True
    # 当参数--testself被指定时, testself为True
    parser.add_argument(
        '--testself',
        action="store_true",
        dest="testself",
        default="",
        help=u"程序自测标识")
    args = parser.parse_args()
    args.keyword = args.keyword.decode("utf-8")

    return args
