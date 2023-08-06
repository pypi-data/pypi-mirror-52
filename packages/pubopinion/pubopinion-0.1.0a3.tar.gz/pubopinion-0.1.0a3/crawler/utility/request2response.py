# utilities for request and response in scrapy.
import json
import logging
import re

xpath_all_links = "//a/@href"


class ResponseUtils:
    @staticmethod
    def get_all_links(response):
        return response.xpath(xpath_all_links).getall()

    @staticmethod
    def jsonp_to_json(jsonp):
        if jsonp is not None:
            try:
                a = re.search(r'[^\(]*\((.*)\)$', jsonp).group(1)
                return json.loads(a)
            except Exception as e:
                err_msg = "JSONP 转换错误"
                print(err_msg, e)
                logging.error(err_msg, e)
