import logging
from datetime import datetime

from analysis.dbutils import select, update_by_id, table_article, select_not_sentiment, select_not_topic
from crawler.db.db import get_connection
from crawler.nlpapi.core import TextAnalyzer, BaiduAnalyzer


def get_hot_spot(limit=20, start=datetime.min, end=datetime.max):
    """Get limit number of hot spots in the time between start and end.
    Of course, the function will select specified number of hot spots between start and end.
    By default, it will select hot spots of all in the database.
    :param limit: number of selecting hot spots, default is 20.
    :param start: start time, default is zero.
    :param end: deadline, default is datetime.max.
    :return: a list of hot spots, it may be less than num, if data is too lack in database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # For getting number of news in specified range of date.
        sql = """
            -- 统计最近一天之内，评论最多的新闻，新闻内容不可为空，如果为空则不显示。
            SELECT 
                COUNT(cpc.id)   AS hot_degree , 
                cpa.create_by   AS source, 
                cpa.title       AS title, 
                cpa.body        AS content, 
                cpa.create_time AS publish_time
            FROM  cadrem_pubopinion_comment AS cpc
            JOIN cadrem_pubopinion_article  AS cpa ON cpa.id = cpc.article_id 
            WHERE 
                cpa.create_time BETWEEN %(start)s AND %(end)s 
                -- AND (cpa.body <> NULL OR cpa.body <> "")
            GROUP BY cpa.id 
            ORDER BY hot_degree DESC 
            LIMIT 0, %(limit)s;
        """
        params = {
            "limit": limit,
            "start": start,
            "end": end,
        }
        success = cursor.execute(sql, params)
        if not success:
            raise Exception("查询未成功！")
        sets = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(e)
        print(e)
    finally:
        if conn is not None:
            conn.close()
    # make data model
    return [
        {"hot_degree": _0, "source": _1, "title": _2, "content": _3, "publish_time": _4}
        for _0, _1, _2, _3, _4 in sets
    ]


class ArticleHandle(object):

    def __init__(self):
        self.analyzer = BaiduAnalyzer()
        pass

    def update_sentiment(self, batch=10):
        affected = 0
        for i in self._sentiment_analyze(batch):
            print(i)
            affected += self._update_sentiment(i)
        return affected

    def _sentiment_analyze(self, batch):
        """
        Analyze sentiment
        :param batch:
        :return:
        """
        for rows in select_not_sentiment(table_article, batch=batch):
            texts = []
            for row in rows:
                text = {
                    "id": row[0],
                    "params": {
                        "text": row[0] + row[3]
                    }
                }
                texts.append(text)
            yield self.analyzer.sentiment_classify(*texts)

    def _update_sentiment(self, results):
        rows = []
        for result in results:
            if result["result"] and "error_code" not in result["result"].keys():
                rows.append({
                    "id": result["id"],
                    "sentiment": result["result"]["items"][0]["sentiment"]
                })
            else:
                logging.error(result)
                print(result)
        return update_by_id(*rows)

    def update_topic(self, batch=10):
        """
        Classify and update database
        :return:
        """
        affetcted_rows = 0
        for i in self._topic_classify(batch):
            affetcted_rows += self._update_topic_classify(i)
        return affetcted_rows

    def _topic_classify(self, batch=100):
        """
        Select has not been classified articles
        :param batch:
        :return: a list of tuples
        """
        for rows in select_not_topic(table=table_article, batch=batch):
            articles = []
            for row in rows:
                article = {
                    "id": row[0],
                    "params": {
                        "title": row[1],
                        "content": row[3]
                    }
                }
                articles.append(article)
            yield self.analyzer.topic(*articles)

    def _update_topic_classify(self, results):
        """
        :param results: [{"id": id, "result": result}, ...]
        :return:
        """
        rows = []
        for result in results:
            if result["result"] and "error_code" not in result["result"].keys():
                response_result = result["result"]
                lv1 = response_result["item"]["lv1_tag_list"]
                lv2 = response_result["item"]["lv2_tag_list"]
                types = {i["tag"] for i in lv1 if i["tag"] != "" or i["tag"] is not None}
                types.update({i["tag"] for i in lv2 if i["tag"] != "" or i["tag"] is not None})
                lv = "|".join(types)
                rows.append({
                    "id": result["id"],
                    "article_type": lv,
                })
            else:
                logging.error(result)
                print(result)
        return update_by_id(*rows)


if __name__ == '__main__':
    handle = ArticleHandle()
    # handle.topic()
    # print("end")
    #
    # for i in handle._topic_classify(1):
    #     print(i)
    #     result = handle._update_topic_classify(i)
    #     print(i)
    handle.update_sentiment(1)