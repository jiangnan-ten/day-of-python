# -*- coding: utf-8 -*-
import sys
import requests
import json
import logging
import time
import MySQLdb
import Queue
import threading
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


def myLog():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='163.log',
                        filemode='w')
    # 控制台日志输出
    console = logging.StreamHandler()
    logging.getLogger("requests").setLevel(logging.WARNING)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return logging.getLogger('one yuan')


class mySql():

    def __init__(self):
        try:
            self.con = MySQLdb.connect(
                host='127.0.0.1', user='root', passwd='111', db='ten', charset="utf8")
            self.cursor = self.con.cursor()
        except Exception, e:
            mylogger.info(e)
            sys.exit()

    def execute(self, sql, key):
        self.cursor.execute(sql, key)
        self.con.commit()

    def findAll(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def closeDb(self):
        self.con.close()

# 分析主页 提取gid, period


def parseMain(url):
    box = []
    content = requests.get(url).content
    soup = BeautifulSoup(content, "lxml")
    li = soup.find_all('li', attrs={'class': 'w-quickBuyList-item'})
    if li:
        for i in li:
            div = i.find('div')
            if div:
                gid = div.get('data-gid')
                period = div.get('data-period')
                box.append({'gid': gid, 'period': period})

    return box

# 装填队列


def queueWork(box):
    queue = Queue.Queue()
    for i in box:
        queue.put(i)

    return queue

# 每个线程执行的任务


def core():
    while True:
        try:
            current_work = queue.get_nowait()
        except:
            break
        else:
            current_gid, current_period = current_work['gid'], current_work['period']
            db = mySql()
            doJob(current_gid, current_period, db)
            db.closeDb()

# 解析json 数据入库


def doJob(gid, period, db):
    while True:
        try:
            if str(period) != str(map.get(int(gid))):
                url = 'http://1.163.com/goods/getPeriod.do?gid=%s&period=%s&navigation=-1' % (
                    str(gid), str(period))
                r = requests.get(url)
                json_data = json.loads(r.content)

                result = json_data['result']
                periodWillReveal = result['periodWillReveal']
                periodWinner = result['periodWinner']
                current_id = str(period)
                if periodWinner:
                    period = str(periodWinner['period'])
                    goods = periodWinner['goods']
                    owner = periodWinner['owner']
                    ownerCost = periodWinner['ownerCost']
                    duobaoTime = periodWinner['duobaoTime']
                    luckyCode = str(periodWinner['luckyCode'])

                    gname = goods['gname']
                    gid = goods['gid']

                    owner_ip = owner['IP']
                    owner_ip_addr = owner['IPAddress']
                    nickname = owner['nickname']
                    cid = str(owner['cid'])
                    avatarPrefix = "%s90.jpeg" % owner['avatarPrefix']

                    sql = "insert into duobao values(0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    key = (gid, gname, period, current_id, nickname, owner_ip, owner_ip_addr,
                           ownerCost, cid, avatarPrefix, duobaoTime, luckyCode)
                    try:
                        db.execute(sql, key)
                    except MySQLdb.Error, e:
                        mylogger.error(e)
                    else:
                        mylogger.info(u"商品%s--%s期==> 中奖用户: %s, ip: %s" %
                                      (gname, period, nickname, owner_ip_addr))
                elif periodWillReveal:
                    period = periodWillReveal['period']
                else:
                    break
            else:
                break
        except:
            break

# 找到对应商品最近的一期


def findExist():
    sql = "select gid, max(current_id) as current_id from duobao group by gid"
    db = mySql()
    return dict(db.findAll(sql))


def getAllUrl(firstPage, lastPage):
    urlbox = []
    for i in range(firstPage, lastPage + 1):
        urlbox.append('http://1.163.com/list/0-0-1-%d.html' % i)

    return urlbox

if __name__ == '__main__':
    mylogger = myLog()
    urlbox = getAllUrl(1, 9)
    if urlbox:
        box = parseMain('http://1.163.com/list/2-0-1-1.html')
        if box:
            queue = queueWork(box)

            # 加入线程池 线程池里面存放4个线程
            threadBox = []

            map = findExist()

            # 线程初始化
            for x in range(1, 15):
                t = threading.Thread(target=core)
                threadBox.append(t)
                t.start()

            # 线程开始工作
            if len(threadBox) > 0:
                for i in threadBox:
                    i.join()

            print "All done!"
        else:
            mylogger(u'首页解析失败')
