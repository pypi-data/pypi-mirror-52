# make it work in both python2 both python3
import json
import logging
import sys
import time

from datetime import datetime

from crawler.nlpapi import config

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# skip https auth
# @TODO: 可能不安全
from crawler.nlpapi.config import ACCOUNTS, AIP_SLEEP_TIME, RETRY_TIMES
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Client:
    """  TOKEN start """
    TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

    def __init__(self):
        self.next = 0
        self.accounts = ACCOUNTS

    def get_aip_config(self):
        """轮询方式获取一个百度接口的配置
        :return:
        """
        pos = self.next
        accounts = self.accounts
        self.next = (pos + 1) % len(accounts)
        cfg = accounts[pos]
        if not hasattr(cfg, "grant_type") or "client_credentials" not in cfg.values():
            cfg["grant_type"] = "client_credentials"
        return {
            "grant_type": cfg["grant_type"],
            "client_id": cfg["api_key"],
            "client_secret": cfg["secret_key"]
        }

    def fetch_token(self):
        """  Fetch Token """
        params = self.get_aip_config()
        post_data = urlencode(params)
        if IS_PY3:
            post_data = post_data.encode('utf-8')
        req = Request(Client.TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            print(err)
        if IS_PY3:
            result_str = result_str.decode()

        result = json.loads(result_str)

        if 'access_token' in result.keys() and 'scope' in result.keys():
            if 'brain_all_scope' not in result['scope'].split(' '):
                print('please ensure has check the  ability')
                exit()
            return result['access_token']
        else:
            print('please overwrite the correct API_KEY and SECRET_KEY')
            exit()

    def request(self, url, data={}):
        """调用百度远程服务
        :param url:
        :param data:
        :return: unicode字符串
        """
        req = Request(url, json.dumps(data).encode())
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()
            if IS_PY3:
                result_str = result_str.decode()
            return result_str
        except URLError as err:
            print(err)
            logging.error(err)


class Aip:
    TOPIC_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/topic"
    SENTIMENT_CLASSIFY_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"

    def __init__(self):
        self.client = Client()
        self.token = None
        self.last_fetch_time = datetime.fromtimestamp(0)

    def _request_raw(self, url, data):
        client = self.client
        if AIP_SLEEP_TIME:
            time.sleep(AIP_SLEEP_TIME)
        response = client.request(url, data)
        # 有时会超时打不开，所以用空对象代替
        return response if response else "{}"

    def _request(self, url, data):
        return json.loads(self._request_raw(url, data))

    def _check_token(self):
        """是否过期"""
        interval = datetime.now() - self.last_fetch_time
        if interval.days > 29:
            return True

    def _fetch_token(self):
        if self._check_token():
            self.token = self.client.fetch_token()
        return self.token

    def _truncate(self, text, max_size, encoding="UTF-8"):
        while len(bytes(text, encoding=encoding)) > max_size:
            text = text[:len(text)-1]
        return text

    def _get_available_url(self, url, encoding="UTF-8"):
        token = self._fetch_token()
        available_url = url+"?charset="+encoding+"&access_token="+token
        return available_url

    def topic(self, title, content):
        """文章分类接口
        参见：https://ai.baidu.com/docs#/NLP-Apply-API/e3191e88
        :param title:
        :param content:
        :return:
        """
        try:
            data = {
                "title": self._truncate(title, max_size=80),
                "content": self._truncate(content, max_size=65535),
            }
            url = self._get_available_url(self.TOPIC_URL)
            resp = self._request_raw(url, data)
            retry_times = 0
            while not resp and retry_times < RETRY_TIMES:
                resp = self._request_raw()
                retry_times += 1
            if not resp:
                logging.error("百度请求接口数据返回异常")
                print("百度请求接口数据返回异常")
            return json.loads(resp if resp else {})
        except (TypeError, Exception) as e:
            logging.error(e)
            print(e)

    def sentiment_classify(self, text):
        """
        情感分析接口
        参见：https://ai.baidu.com/docs#/NLP-Apply-API/955c17f6
        :param text: less than 2048 bytes
        :return:
        """
        data = {
            "text": self._truncate(text, max_size=2048)
        }
        url = self._get_available_url(self.SENTIMENT_CLASSIFY_URL)
        return self._request(url, data)


class Constants(object):
    SENTIMENT_NEGATIVE = 0
    SENTIMENT_NORMAL = 1
    SENTIMENT_POSITIVE = 2
    TOPIC_CLASS = [
        "国际", "体育", "娱乐", "社会", "财经", "时事", "科技", "情感", "汽车", "教育", "时尚", "游戏", "军事", "旅游",
        "美食", "文化", "健康养生", "搞笑", "家居", "动漫", "宠物", "母婴育儿", "星座运势", "历史", "音乐", "综合",
    ]


if __name__ == '__main__':
    # client = Client()
    start = time.time()
    # for i in range(100):
    #     client.fetch_token()
    aip = Aip()
    text = "".join(["a" for i in range(2049)])
    a = aip.sentiment_classify(text=text)
    print(a)
    end = time.time()
    print(end - start)
