from collections import namedtuple

from crawler.db.db import StorageDAO
from crawler.nlpapi.baidu_aip import Aip, Constants
from crawler.utility.preprocesss import strip_tags


class TextAnalyzer(object):
    def __init__(self):
        self.aip = Aip()
        pass

    def topic(self, *articles):
        result = []
        if articles is None:
            return result
        for article in articles:
            result.append(self._topic_one(article))
        return result

    def _topic_one(self, article):
        return [self.aip.topic(title=article["title"], content=article["content"]), article]

    def _sentiment_classify_one(self, text):
        return [self.aip.sentiment_classify(text=text), text]

    def sentiment_classify(self, *texts):
        result = []
        if texts is None:
            return result
        for text in texts:
            result.append(self._sentiment_classify_one(text))
        return result


class Texts:
    analyzer = TextAnalyzer()

    def __init__(self):
        pass

    @staticmethod
    def sentiment(*texts):
        if texts is None or len(texts) < 1:
            return None
        results = Texts.analyzer.sentiment_classify(*texts)
        negative = 0  # 负向0
        normal = 0    # 中性1
        positive = 0  # 正向2
        for r, text in results:
            items = r["items"]
            for item in items:
                sentiment = item["sentiment"]
                if sentiment == Constants.SENTIMENT_NEGATIVE:
                    negative += 1
                elif sentiment == Constants.SENTIMENT_NORMAL:
                    normal += 1
                elif sentiment == Constants.SENTIMENT_POSITIVE:
                    positive += 1
        amounts = len(texts)
        return [negative/amounts, normal/amounts, positive/amounts]

    @staticmethod
    def topic(*articles):
        results = analyzer.topic(*articles)
        statistic = dict()
        for clazz in Constants.TOPIC_CLASS:
            statistic[clazz] = dict()
            statistic[clazz]["total"] = 0
            statistic[clazz]["articles"] = []
        for analysis_result, article in results:
            item = analysis_result["item"]
            lv1_tag_list = item["lv1_tag_list"]
            # lv2_tag_list = item["lv2_tag_list"]
            for lv1 in lv1_tag_list:
                if lv1["tag"] in statistic.keys():
                    statistic[lv1["tag"]]["articles"].append([analysis_result, article])
                    statistic[lv1["tag"]]["total"] += 1
        return statistic


class BaiduAnalyzer(object):
    def __init__(self):
        self.analyzer = Aip()

    def topic(self, *articles):
        """
        Classify for topics of articles
        :param articles: a list of mappings, for example:
            [{"id": id, "params": {"title": title, "content":content}}, ...]
        :return: A list of mappings that composed as [{"id": id, "result": result}, ...]
        """
        result = []
        for article in articles:
            params = article["params"]
            resp = self.analyzer.topic(title=params["title"], content=params["content"])
            result.append({"id": article["id"], "result": resp})
        return result

    def sentiment_classify(self, *texts):
        """
        Analyze sentiment of texts
        :param texts: A list of mappings, for example, [{"id": id, "params": {"text": text}}, ...]
        :return: A list of mappings, for example, ["id": id, "result": result]
        """
        result = []
        for text in texts:
            params = text["params"]
            resp = self.analyzer.sentiment_classify(text=params["text"])
            result.append({"id": text["id"], "result": resp})
        return result


if __name__ == '__main__':
    analyzer = TextAnalyzer()
    topic0 = {
        "title": "识别输入文本中有错误的片段",
        "content": "识别输入文本中有错误的片段，提示错误并给出正确的文本结果。支持短文本、长文本、语音等内容的错误识别，纠错是搜索引擎、语音识别、内容审查等功能更好运行的基础模块之一。",
    }
    topic1 = {
        "title": "识别输入文本中有错误的片段",
        "content": "识别输入文本中有错误的片段，提示错误并给出正确的文本结果。支持短文本、长文本、语音等内容的错误识别，纠错是搜索引擎、语音识别、内容审查等功能更好运行的基础模块之一。",
    }

    # result0 = analyzer.topic(topic0, topic1)
    # print(result0)
    text0 = "苹果是一家伟大的公司"
    text1 = "苹果是一家伟大的公司"
    # result1 = analyzer.sentiment_classify(text0, text1)
    # print(result1)
    # result3 = Texts.sentiment(topic0, topic1)
    # print(result3)
    # print(analyzer.sentiment_classify(text0))
    # result4 = Texts.topic(topic0, topic1)
    # print(result4)
    # dao = StorageDAO()
    # records = dao.select_named(1000, 100)
    # pages = [strip_tags(record.text) for record in records]
    # for page in pages:
    #     print(page+"\n")

    articles = [
        {
            "id": "1",
            "params": {
                "title": topic0["title"],
                "content": topic0["content"]
            }
        },
        {
            "id": "2",
            "params": {
                "title": topic1["title"],
                "content": topic1["content"],
            }
        }
    ]

    texts = [
        {
            "id": "1",
            "params": {
                "text": text0
            }
        },
        {
            "id": "1",
            "params": {
                "text": text1
            }
        }
    ]

    analyzer = BaiduAnalyzer()
    # print(analyzer.topic(*articles))
    # print(analyzer.sentiment_classify(*texts))
