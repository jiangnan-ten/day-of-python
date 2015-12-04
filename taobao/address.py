# -*- coding: utf-8 -*-
import sys
import json
from city import city
from province import province
import Queue
import threading
import time
import logging
import requests
import re
import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")

queue = Queue.Queue()

# 省格式化为字典
province_format = {}
for _, v in province.items():
    for i in v:
        province_format[i[0]] = u'%s' % i[1][0]


city_format = {}

# 处理城市为字典 省号做key
for province_key, province_name in province_format.items():
    temp = {}
    for c in city:
        if c[2] == province_key:
            city_format[province_key] = {
                'name': province_name,
                'city': temp
            }

            city_format[province_key]['city'].update({c[0]: {
                'name': u'%s' % c[1][0],
                'city': {}
            }})

for p_code, p_v in city_format.items():
    for c_code, c_v in p_v['city'].items():
        for x in city:
            if c_code == x[2]:
                city_format[p_code]['city'][c_code]['city'].update({
                    x[0]: x[1][0]
                })


for k, v in city_format.items():
    for m, n in v['city'].items():
        for x, y in n['city'].items():
            queue.put({
                'l1': {'code': k, 'name': v['name']},
                'l2': {'code': m, 'name': n['name']},
                'l3': {'code': x, 'name': u'%s' % y}
            })

# 当前线程处理的内容


def core():
    threadName = threading.current_thread().name
    # print u'当前线程=> %s' % threadName
    while True:
        try:
            current_work = queue.get_nowait()
        except:
            break

        try:
            l1 = current_work['l1']['code']
            l2 = current_work['l2']['code']
            l3 = current_work['l3']['code']

            l1_name = current_work['l1']['name']
            l2_name = current_work['l2']['name']
            l3_name = current_work['l3']['name']

            url = 'https://lsp.wuliu.taobao.com/locationservice/addr/output_address_town_array.do?l1=%s&l2=%s&l3=%s' % (
                l1, l2, l3)

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
                'cookie': "cna=M9urDhjZGBYCAXbyGtqOKCFP; thw=cn; miid=7206575810382719403; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; v=0; _tb_token_=p5XQbwKR1p; uc3=nk2=sHFEbHGsVNP08J8%3D&id2=VAcPSx87zHIk&vt3=F8dAScAYb14u9c4K7JU%3D&lg2=UIHiLt3xD8xYTw%3D%3D; existShop=MTQ0OTE5MjMxNA%3D%3D; lgc=%5Cu7389%5Cu4F69%5Cu5929%5Cu6DAF%5Cu8FDC1; tracknick=%5Cu7389%5Cu4F69%5Cu5929%5Cu6DAF%5Cu8FDC1; sg=148; cookie2=1c5d1d3ce557d88b2a02142a7706278e; mt=np=&ci=-1_1; cookie1=AQWYaUCnbVAnmXYmpnDAyOaTpH8CN2F2IvNupBA%2F6lQ%3D; unb=761754554; skt=33b1a69d4284e126; t=1125a2a6aeef48766b114aa2b5223118; publishItemObj=Ng%3D%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu7389%5Cu4F69%5Cu5929%5Cu6DAF%5Cu8FDC1; cookie17=VAcPSx87zHIk; uc1=cookie14=UoWzUGXGX1%2BS6Q%3D%3D&existShop=false&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=VFC%2FuZ9ainBZ&tag=7&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; isg=FF788A42DDDF5E2E691217184CC08FCE; l=Ajw8SH9D-LTSBiSTxq0u90OrjNTuwuBe",
                'referer': 'https://member1.taobao.com/member/fresh/deliver_address.htm?spm=a1z02.1.972272805.d4912033.yHi6Ff'
            }
            res = requests.get(url, headers=headers)
            content = res.content
        except:
            logger.info(u'%s-%s-%s 没有响应' % (l1, l2, l3))
        else:
            re_result = re.findall(r"'(\d{9})','(.*?)'", content)
            sql = "insert into taobao values"
            if re_result:
                for i in re_result:
                    # print l1, l2, l3, i[0], u'%s' % i[1]
                    sql += "(0, '%s', '%s', '%s', '%s')," % (
                        l1_name, l2_name, l3_name, u'%s' % i[1]
                    )
                sql = sql[:-1]

                try:
                    mysql = mySql()
                    mysql.execute(sql)

                    logger.info("%s-%s-%s插入成功" % (l1, l2, l3))
                except MySQLdb.Error, e:
                    logger.error(e)
            else:
                logger.info("%s-%s-%解析失败" % (l1, l2, l3))

        finally:
            time.sleep(2.5)

threadBox = []


class mySql():

    def __init__(self):
        try:
            self.con = MySQLdb.connect(
                host='127.0.0.1', user='root', passwd='', db='test2', charset="utf8")
            self.cursor = self.con.cursor()
        except Exception, e:
            logger.info(e)
            sys.exit()
        else:
            pass
            # logger.info(u'连接数据库成功')

    def execute(self, sql):
        self.cursor.execute(sql)
        self.con.commit()
        self.closeDb()

    def closeDb(self):
        self.con.close()
        # logger.info(u'数据库关闭')


def mylog():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='taobao.log',
                        filemode='w')
    # 控制台日志输出
    console = logging.StreamHandler()
    logging.getLogger("requests").setLevel(logging.WARNING)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return logging.getLogger('taobao')

logger = mylog()

for x in range(1, 10):
    t = threading.Thread(target=core, name='thread-%d' % x)
    threadBox.append(t)
    t.start()

if len(threadBox) > 0:
    for i in threadBox:
        i.join()

print "done"

# print json.dumps(city_format, indent=4)
