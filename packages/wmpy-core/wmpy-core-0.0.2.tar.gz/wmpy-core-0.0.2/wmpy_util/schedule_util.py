#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : schedule_util.py
@Desc    : 定时任务
"""
import time
import threading
import schedule


class ScheduleManger:
    def __init__(self, interval=1):
        self._quaz_flag = True
        self._interval = interval
        self._thread = threading.Thread(target=self.do_work)
        self._thread.daemon = True
        self._thread.start()

    def do_work(self):
        while self._quaz_flag:
            time.sleep(self._interval)
            schedule.run_pending()

    def stop_timer(self):
        self._quaz_flag = False

    def add_schedule(self, every, job, args=(), kwargs={}):
        """
        增加定时任务
        :param every: 时间间隔：秒
        :param job:
        :param args:
        :param kwargs:
        :return:
        """
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = dict()
        if not isinstance(args, list) and not isinstance(args, tuple):
            args = (args,)
        schedule.every(every).seconds.do(job, *args, **kwargs)


schedule_manager = ScheduleManger()





if __name__ == '__main__':
    def my_job(name, *args, **kwargs):
        print(args, kwargs)
        print("my name is %s, at %.2f" % (name, time.time()))
    s = ScheduleManger()
    s.add_schedule(6, my_job, ("zww", "haha", 123), dict(a=1, b=2))
    s.add_schedule(3, my_job, ("ly", "lala", "456"), dict(jaja=1))
    time.sleep(10)
    s.add_schedule(1, my_job, ("yx", "jiji", 222), dict(bibi=2))
    a = input()
    s.stop_timer()
    time.sleep(100)
