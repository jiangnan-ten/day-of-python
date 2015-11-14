# -*- coding: utf-8 -*-

'''
多线程 抓取拉勾网上海php数据
'''

import sys
import threading
import Queue
import logging
import json
import requests
import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")


class mySql():

    def __init__(self):
        try:
            self.con = MySQLdb.connect(
                host='127.0.0.1', user='root', passwd='', db='test', charset="utf8")
            self.cursor = self.con.cursor()
        except Exception, e:
            logger.info(e)
            sys.exit()
        else:
            logger.info(u'连接数据库成功')

    def execute(self, sql):
        self.cursor.execute(sql)
        self.con.commit()
        self.closeDb()

    def closeDb(self):
        self.con.close()
        logger.info(u'数据库关闭')


class myThreading(threading.Thread):

    def __init__(self, func):
        super(myThreading, self).__init__()
        self.func = func

    def run(self):
        self.func()


class Mylogger():

    def begin(self):
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='lagou2.log',
                            filemode='w')
        # 控制台日志输出
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        return logging.getLogger('lagou')


class crawer():

    def __init__(self, url):
        self.url = url
        self.__init__queuePool()
        self.parseMainUrl()

    def __init__queuePool(self):
        self.workQueue = Queue.Queue()

    def __toQueue(self, totalPageCount):
        for i in range(1, totalPageCount+1):
            self.workQueue.put({
                'first': 'true' if i == 1 else 'false',
                'pn': i,
                'kd': 'php'
            })

    def __create_threadPool(self, threadNum):
        self.threads = []
        for i in range(threadNum):
            t = myThreading(self.core)
            t.start()
            self.threads.append(t)

    # 解析url
    def parseMainUrl(self):
        r = requests.post(self.url, data={
            'first': 'true',
            'pn': 1,
            'kd': 'php'
        })

        try:
            py_data = json.loads(r.text)
            self.totalPageCount = totalPageCount = py_data['content']['totalPageCount']
            self.totalCount = totalCount = py_data['content']['totalCount']

            logger.info("总计: %d条数据, %d页" % (totalCount, totalPageCount))
        except:
            logger.info('url请求解析失败')
            sys.exit()
        else:
            if totalCount > 0:
                self.start()

    def start(self):
        # 根据页数决定开启的线程数
        threadNum = 1
        if self.totalCount == 1:
            threadNum = 1
        elif 1 <= self.totalPageCount < 10:
            threadNum = 5
        elif 10 <= self.totalPageCount < 50:
            threadNum = 15
        else:
            threadNum = 25

        # 装填队列
        self.__toQueue(self.totalPageCount)

        # 创建线程池 开启
        self.__create_threadPool(threadNum)

    def core(self):
        while True:
            try:
                task_in_queue = self.workQueue.get_nowait()
                print task_in_queue['pn']
            except:
                break

            try:
                r = requests.post(self.url, data=task_in_queue)
                py_data = json.loads(r.text)
                result = py_data['content']['result']
                pasgeSize = py_data['content']['pageSize']

                sql = "insert into lagou values"

                for i in result:
                    sql += "(0, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')," % (
                        i['companyShortName'],
                        i['companyName'],
                        i['positionName'],
                        i['workYear'],
                        i['education'],
                        i['financeStage'],
                        i['industryField'],
                        i['city'],
                        i['salary'],
                        i['companySize']
                    )

                sql = sql[:-1]

            except:
                logger.info("第%d页数据请求失败" % task_in_queue['pn'])

            try:
                mysql = mySql()
                mysql.execute(sql)

                logger.info("第%d页%d条数据入库成功" % (task_in_queue['pn'], pasgeSize))
            except MySQLdb.Error, e:
                logger.error(e)

if __name__ == '__main__':
    logger = Mylogger().begin()  # 开启日志
    url = 'http://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7'

    crawer(url)
