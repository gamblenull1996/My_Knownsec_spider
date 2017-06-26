# My_Knownsec_spider

知道创宇爬虫
##### v1 支持 -u -d --dbfile
- args_parser.py 处理命令行参数
- database.py 数据库相关操作
- spider.py 爬虫主体

在命令行中运行，结果如下

`python spider.py -u http:www.baidu.com -d 2 --dbfile baidu.db`

![baidu](img/baidu.png)

##### v1.1 支持页面内的相对链接
测试页面 https://docs.python.org/2/library/urlparse.html
从该页面提取的出的链接存放在result.txt中，经过比对，正确找出了页面中的相对链接和以http开头的链接。

#### Todo
程序每隔10秒在屏幕上打印进度信息
