# -*- coding: utf-8 -*-
import sys
import requests
import Queue
import threading
import os
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


def getAllUrl(url, page):
    urlBox = []
    for i in range(1, page + 1):
        urlBox.append("%s%i.html" % (url, i))

    return urlBox


def spider(url):
    text = requests.get(url).text
    soup = BeautifulSoup(text)


def myThread():
    # 当前的线程名
    threadName = threading.current_thread().name
    while True:
        try:
            # 当前线程即将处理的url
            currentUrl = queue.get_nowait()
            filename = '%s/%s.text' % (path, currentUrl[-6])

            f = open(filename, 'w+')

            res = requests.get(currentUrl)
            if res:
                html = res.content
                if html:
                    soup = BeautifulSoup(html)
                    parent = soup.find_all('div', attrs={'class': 'articleCell SG_j_linedot1'})
                    if parent:
                        for i in parent:
                            node = i.find_all('a')[-1]

                            text = node.get_text()
                            href = node.get('href')

                            f.write("%s %s \r\n" % (text, href))

                    f.close()
                else:
                    print u"%s 解析失败" % currentUrl
            else:
                print u"%s 发送请求失败" % currentUrl
        except:
            break


if __name__ == '__main__':
    # 创建目录存储
    path = './dir'
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print u'目录创建成功 名称dir'

    urlBox = getAllUrl('http://blog.sina.com.cn/s/articlelist_1191258123_0_', 7)

    # 开启队列
    queue = Queue.Queue()
    for i in urlBox:
        queue.put(i)

    # 加入线程池 线程池里面存放4个线程
    threadBox = []

    # 线程初始化
    for x in range(1, 5):
        t = threading.Thread(target=myThread, name='thread-%d' % x)
        threadBox.append(t)
        t.start()

    # 线程开始工作
    if len(threadBox) > 0:
        for i in threadBox:
            i.join()

    print "done"
