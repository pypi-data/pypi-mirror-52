import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from crawler.items import HTMLItem
from crawler.spiders.config import keywords
from urllib.parse import urlencode
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaiduNewsSpider(RedisSpider):

    name = "BaiduNewsSpider"
    BASE_URL = "https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&tn=news&rsv_sug3=1&rsv_sug4=111&" \
               "rsv_sug1=1&f=3&rsp=1"

    request_params = {
        "ie": "utf-8",
        "cl": 2,
        "medium": 0,
        "rtt": 1,
        "bsst": 1,
        "tn": "news",
        "word": "贵阳",
        "rsv_sug3": 1,
        "rsv_sug4": 111,
        "rsv_sug1": 1,
        "f": 3,
        "rsp": 1,
        "rsv_dl": "news_b_pn",  # 首次有，但第二次变化，以后不变
        "x_bfe_rqs": "03E80",   # 首次没有，第二次有，以后不变
        "x_bfe_tjscore": "0.002032",  # 首次无，第二次有，以后变化
        "tngroupname": "organic_news",  # 首次无，以后有，第二次以后不变
        "pn": 0,  # 首次无，第二次有，以后变化 => 页面第一条结果在结果中的偏移量
    }

    def start_requests(self):
        for starting_url in self.get_starting_urls():
            yield Request(url=starting_url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        for req in self.crawl_items(response):
            yield req
        for req in self.crawl_search_pages(response):
            yield req

    def crawl_items(self, response):
        links = response.xpath('//*[@id="content_left"]//a/@href')
        for link in links:
            yield response.follow(url=link, callback=self.download_page)

    def crawl_search_pages(self, response):
        links = response.xpath('//*[@id="page"]//a/@href')
        for link in links:
            yield response.follow(url=link, callback=self.crawl_items)

    def download_page(self, response):
        item = HTMLItem()
        text = response.xpath('//html/text()').getall()
        item["url"] = response.url
        item["text"] = text
        yield item

    def get_starting_urls(self):
        base_url = BaiduNewsSpider.BASE_URL
        # 主关键词
        main_words = keywords["main"]
        # 副关键词
        second_words = keywords["second"]
        # 组合每一个主关键词
        for mw in main_words:
            for sw in second_words:
                starting_url = base_url + "&" + urlencode({"word": mw + "+" + sw})
                yield starting_url
