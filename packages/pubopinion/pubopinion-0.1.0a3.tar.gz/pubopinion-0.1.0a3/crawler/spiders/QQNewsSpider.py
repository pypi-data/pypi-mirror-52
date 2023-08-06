import json
import logging
import re
from urllib.parse import urlencode, parse_qs, urlparse, urljoin

import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from crawler.items import QQNewsItem
from crawler.utility.request2response import ResponseUtils as ru


class QQNewsSpider(scrapy.Spider):
    name = "QQNewsSpider"
    urls = ["https://news.qq.com/"]
    re_news = r"(?i:https?://new\.qq\.com/.*(?=html))"
    xpath_all_links = "//a/@href"
    xpath_news_detail = "/html/body/div[3]/div[1]/div[1]/div[2]//text()"

    # 热点精选
    base_url = "https://pacaio.match.qq.com/irs/rcd"
    # 今日要闻
    jin_ri_yao_wen = "https://i.match.qq.com/ninja/fragcontent?pull_urls=news_top_2018&callback=__jp0"
    # 热点精选
    re_dian_jing_xuan = "https://pacaio.match.qq.com/irs/rcd?cid=137&id=&ext=top&page=0&expIds=&callback=__jp1"
    # 热门资讯 cid=4是热门资讯，cid=137是热点精选
    # 该链接token必须存在，应该根据index.js中的cid=xxx&token=去搜索除token
    re_men_zi_xvn = "https://pacaio.match.qq.com/irs/rcd?cid=4&token=9513f1a78a663e1d25b46a826f248c3c&ext=&page=0&expIds=&callback=__jp2"
    # index.js 用来获取token
    index_js_url = "https://mat1.gtimg.com/pingjs/ext2020/newom/build/static/js/index.js"
    # index.js
    index_js = ""
    tokens = []
    cids = ['137']
    # parameters template
    param_tmp0 = {
        "cid": 0,               # 数字
        "token": "",            # index.js 中，使用cid=xxx&token=找寻
        "id": "",               #
        "ext": "top",           # ext = 0 if cid == '137'
        "expIds": "",           # 某些链接下上一个链接中的所有新闻名字取日期+紧接6位字母的分割，例如：20190101ABCDEF|...
        "callback": "__jp1",    # 回调函数名称
    }
    re_news_url = r"(?i:https?://new\.qq\.com.*(?=\.html))"
    comments_url = r'https://coral.qq.com/article/4157351119/comment/v2?callback=_article4157351119commentv2&orinum=1&oriorder=o&pageflag=1&cursor=0&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1568249359993'

    custom_settings = {

    }

    def __init__(self, *args, **kwargs):
        super(QQNewsSpider, self).__init__(*args, **kwargs)
        self.count = 0

    def start_requests(self):
        yield self.download_index_js()

    def download_index_js(self):
        index_js = QQNewsSpider.index_js_url
        return Request(url=index_js, callback=self.parse_index_js, dont_filter=True)

    def parse_index_js(self, response):
        js = QQNewsSpider.index_js = response.text
        QQNewsSpider.tokens = [
            {"cid": cid, "token": token}
            for x in re.findall(r'cid=[\d]*&token=[\w]+', js)
            for cid, token in [
                [y.split("=")[1] for y in x.split("&")]
            ]
        ]
        # for req in self.download_jin_ri_yao_wen(response):
        #     yield req
        for req in self.download_channels(response, QQNewsSpider.cids):
            yield req
        # print("===================================")
        # for req in self.test_download_comments(response):
        #     print(req)
        #     yield req

    def download_jin_ri_yao_wen(self, response):
        yield response.follow(QQNewsSpider.jin_ri_yao_wen, callback=self.parse_jin_ri_yao_wen, dont_filter=True)

    def parse_jin_ri_yao_wen(self, response):
        logging.debug("======解析《今日要闻》=======")
        items = ru.jsonp_to_json(response.text)
        for item in items:
            meta = dict(response.meta)
            meta["list_info"] = item
            url = item["url"]
            if self._match_new_url(url):
                yield response.follow(url, meta=meta, callback=self.parse_news_detail)

    def parse_news_detail(self, response):
        meta = response.meta
        text = response.text
        pattern = r"(?i:\s*window.DATA\s*=\s*(\{*(\n.*)+?\s+)(?=</script>))"
        match = re.search(pattern, text)
        if match:
            text = match.group(1)
            detail = json.loads(text)
            detail["text"] = "".join(response.xpath("/html/body/div[3]/div[1]/div[1]/div[2]//p/text()").getall())
            meta["detail"] = detail
            for req in self.download_comments(response):
                yield req

    def download_comments(self, response):
        logging.debug("=========================================================")
        logging.debug("====================爬取评论===============================")
        meta = response.meta
        params = {'orinum': '30', 'oriorder': 'o', 'pageflag': '1',
                  'cursor': '0', 'scorecursor': '0', 'orirepnum': '30',
                  'reporder': 'o', 'reppageflag': '1',
                  'source': '1', '_': '1568249359993'}
        detail = meta["detail"]
        comment_id = detail["comment_id"]
        params["callback"] = '_article%scommentv2' % comment_id
        base_url = "https://coral.qq.com/article/%s/comment/v2"
        url = (base_url + "?" + urlencode(params)) % comment_id
        meta["comments"] = []
        yield response.follow(url, meta=meta, callback=self.download_comments_remaining)

    def download_comments_remaining(self, response):
        logging.debug("==========================爬取剩余的评论==========================")
        meta = response.meta
        data = ru.jsonp_to_json(response.text)
        meta["comments"].append(data)
        if "oriCommList" in data["data"].keys() and len(data["data"]["oriCommList"]) < 30:
            yield self.extract_item(meta)
        else:
            qs = parse_qs(urlparse(response.url)[4])
            qs["cursor"] = data["data"]["last"]
            url = urljoin(response.url, "?" + urlencode(qs, True))
            yield response.follow(url, meta=meta, callback=self.download_comments_remaining)

    def extract_item(self, meta):
        item = QQNewsItem()
        item["meta"] = meta
        return item

    def download_re_dian_jing_xuan(self, response, cid):
        meta = response.meta
        if "params" not in meta.keys():
            params = dict(QQNewsSpider.param_tmp0)
            tokens = QQNewsSpider.tokens
            params["cid"] = cid
            params["token"] = [item["token"] for item in tokens if item["cid"] == params['cid']][0]
            params["ext"] = "top"
            params["callback"] = "__jp1"
            params["page"] = 0
        else:
            params = meta["params"]
            params["page"] += 1
        url = QQNewsSpider.base_url + "?" + urlencode(params)
        yield response.follow(url, meta={"params": params}, callback=self.parse_re_dian_jing_xuan0)

    def parse_re_dian_jing_xuan0(self, response):
        list_info = ru.jsonp_to_json(response.text)
        if "data" in list_info.keys() and len(list_info["data"]) > 0:
            for req in self.download_re_dian_jing_xuan(response, response.meta["params"]["cid"]):
                yield req
        for req in self.parse_re_dian_jing_xuan(response):
            yield req

    def parse_re_dian_jing_xuan(self, response):
        list_info = ru.jsonp_to_json(response.text)
        if "data" in list_info.keys():
            for item in list_info["data"]:
                meta = dict()
                meta["list_info"] = item
                yield response.follow(url=item["vurl"], meta=meta, callback=self.parse_news_detail)
        else:
            logging.warning("Can not parse text: [url => %s ]" % response.url)

    def _match_new_url(self, url):
        if re.search(QQNewsSpider.re_news, url):
            return True

    def download_channels(self, response, cids):
        for cid in cids:
            for req in self.download_re_dian_jing_xuan(response, cid):
                yield req

    # def test_download_comments(self, response):
    #     response.meta["detail"] = {
    #             "comment_id": "4157351119",
    #     }
    #     for req in self.download_comments(response):
    #         yield req
