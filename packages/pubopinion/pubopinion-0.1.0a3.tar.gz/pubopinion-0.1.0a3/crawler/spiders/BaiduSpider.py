# 从百度搜索引擎爬取数据
import logging
from collections import Iterable

import pymysql
import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from crawler.items import HTMLItem

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaiduSpider(RedisSpider):

    name = 'BaiduSpider'

    def start_requests(self):
        return self.get_starting_request(keywords=['阿里云'])

    def get_starting_request(self, keywords=None):
        if keywords is None:
            logger.debug("Keywords are None!")
            return None
        if not isinstance(keywords, Iterable):
            logger.warning("keywords aren't type of Iterable!")
            return None
        wd = ' '.join(keywords)
        search_url = 'https://www.baidu.com/s?ie=utf-8&wd=%s' % wd
        req = Request(url=search_url, callback=self.handle_baidu_page)
        return [req]

    def handle_baidu_page(self, response):
        # 百度搜索页链接抽取
        s_urls = response.xpath('//a/@href').re(r'/s\?.*')
        for su in s_urls:
            yield response.follow(url=su, callback=self.handle_baidu_page)
        i_urls = response.xpath('//*[@id="content_left"]//a/@href').getall()
        # 百度结果页链接抽取
        for iu in i_urls:
            yield response.follow(url=iu, callback=self.handle_specific_website)

    def handle_specific_website(self, response):
        # 保存
        item = HTMLItem()
        item['url'] = response.url
        item['text'] = response.text
        yield item

# if __name__ == '__main__':
#     bs = BaiduSpider()
#     req = bs.get_starting_request(['阿里云'])
#     print(req.url)