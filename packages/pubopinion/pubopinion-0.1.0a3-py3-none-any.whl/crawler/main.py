import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.cmdline import execute

import os
import sys

from analysis.service import PublicOpinionService


class ModuleStarter:

    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.service = PublicOpinionService()
        self.scheduler.add_job(self._execute_crawler, "interval", minutes=30)
        self.scheduler.add_job(self._analyze, "interval", minutes=30)

    def _analyze(self):
        self.service.update()

    def _execute_crawler(self):
        sys.path.append(os.path.abspath(__file__))
        execute(["scrapy", "crawl", "QQNewsSpider"])

    def start(self):
        self.scheduler.start()


if __name__ == '__main__':
    starter = ModuleStarter()
    starter.start()
    # starter._execute_crawler()
    # starter._analyze()
