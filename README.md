# My_Knownsec_spider

知道创宇爬虫
##### v1 支持数据库 -u -d --dbfile
- args_parser.py 处理命令行参数
- database.py 数据库相关操作
- spider.py 爬虫主体

在命令行中运行，结果如下

`python spider.py -u http:www.baidu.com -d 2 --dbfile baidu.db`

![baidu](img/baidu.png)

##### v1.1 支持页面内的相对链接，支持线程池，支持log文件
使用urlparse中的urljoin来提取页面内的相对链接
- log_setting.py 配置logging
- my_threadpool.py 线程池实现

测试页面: https://docs.python.org/2/library/urlparse.html
测试命令:`python .\spider.py -u https://docs.python.org/2/library/urlparse.html -d 2 --dbfile python.db --thread 10 -f python.log -l 5`
从该页面提取的出的链接存放在result.txt中，经过比对，正确找出了页面中的相对链接和以http开头的链接。

#### Todo
程序每隔10秒在屏幕上打印进度信息
