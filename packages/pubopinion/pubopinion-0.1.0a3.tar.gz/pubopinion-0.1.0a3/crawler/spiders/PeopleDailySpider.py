import re

import scrapy as scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider


class PeopleDaily(RedisSpider):
    name = "PeopleDailySpider"

    start_urls = ["http://www.people.com.cn/"]

    def start_requests(self):
        for url in PeopleDaily.start_urls:
            yield Request(url=url, callback=self.parse0)

    def parse0(self, response):
        pass