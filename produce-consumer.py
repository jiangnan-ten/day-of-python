# -*- coding: utf-8 -*-
# 生产者 消费者模型
# 
# 
# 



import sys
import Queue
import threading
import random
import time

reload(sys)
sys.setdefaultencoding("utf-8")

queue = Queue.Queue()


class produce(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                if queue.qsize() == 0:
                    item = random.choice(range(10))
                    queue.put(item)
                    print 'Produce => %d\n' % item
                    time.sleep(1)
            except:
                pass


class consumer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                if queue.qsize() > 0:
                    pop_item = queue.get()
                    print 'Consumer => %d\n' % pop_item
                    time.sleep(1)
            except:
                pass

produce().start()
consumer().start()
