# -*- coding: utf-8 -*-
import sys
import requests
import json
import logging
import time

reload(sys)
sys.setdefaultencoding("utf-8")
sys.setrecursionlimit(3000)


def mylog():
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


def run(gid, period):
    while True:
        try:
            if period:
                url = 'http://1.163.com/goods/getPeriod.do?gid=%s&period=%s&navigation=-1' % (str(gid), str(period))
                r = requests.get(url)
                json_data = json.loads(r.content)

                result = json_data['result']
                period = result['periodWinner']['period']
                goods = result['periodWinner']['goods']
                owner = result['periodWinner']['owner']

                gname = goods['gname']
                owner_ip = owner['IP']
                owner_ip_addr = owner['IPAddress']
                nickname = owner['nickname']
                cid = owner['cid']
                avatarPrefix = "%s_90.jpeg" % owner['avatarPrefix']
                mylogger.info(u"%s期==> 中奖用户: %s, ip: %s" % (period, nickname, owner_ip_addr))
        except:
            break

if __name__ == '__main__':
    mylogger = mylog()
    run(510, 212051353)
