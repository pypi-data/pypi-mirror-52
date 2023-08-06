# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from datetime import datetime

from crawler.model.tables import Article, Comment
from crawler.db import db
from crawler.items import HTMLItem, QQNewsItem


class PublicOpinionCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class TextPipeline(object):
    count = 0

    def process_item(self, item, spider):
        if isinstance(item, HTMLItem):
            self.store_item(self.clean_item(item), spider)
        # else:
        # return DropItem()

    def store_item(self, item, spider):
        sql = "INSERT INTO `text`(`url`, `text`) VALUE(%s, %s)"
        conn = db.get_connection()
        cursor = conn.cursor()
        r = cursor.execute(sql, [item['url'], item['text']])
        conn.commit()
        TextPipeline.count += 1
        if r:
            print('=================Yes======', TextPipeline.count)
        conn.close()

    def clean_item(self, item):
        return item


class MetaItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, QQNewsItem):
            self.store_item(item, spider)

    def store_item(self, item, spider):
        try:
            meta = item["meta"]
            conn = db.get_connection()
            li = meta["list_info"]
            detail = meta["detail"]
            article = {
                "id": detail["article_id"],
                "title": li["title"],
                "body": detail["text"],
                "release_time": datetime.strptime(li["publish_time"], "%Y-%m-%d %H:%M:%S"),
                "create_by": li["source"],
                "create_time": datetime.strptime(li["publish_time"], "%Y-%m-%d %H:%M:%S"),
                "update_by": li["source"],
                "update_time": datetime.strptime(li["update_time"], "%Y-%m-%d %H:%M:%S"),
            }
            sql = "INSERT INTO `cadrem_pubopinion_article`(`id`,`title`,`article_type`," \
                  "`body`,`release_time`,`create_by`,`create_time`, `update_by`, `update_time`) " \
                  "VALUE(%(id)s, %(title)s, DEFAULT, %(body)s, %(release_time)s, %(create_by)s, %(create_time)s, " \
                  "%(update_by)s, %(update_time)s)"
            cursor = conn.cursor()
            self._delete_exists(conn, article["id"])
            cursor.execute(sql, article)
            comments = []
            sql = "INSERT INTO `cadrem_pubopinion_comment`(`id`,`article_id`,`comment`,`create_by`,\
                `create_time`,`update_by`,`update_time`) VALUES(DEFAULT, %(article_id)s, %(comment)s," \
                  "%(create_by)s, %(create_time)s, %(update_by)s, %(update_time)s)"
            for comment in meta["comments"]:
                for c in comment["data"]["oriCommList"]:
                    cc = {
                        "article_id": detail["article_id"],
                        "comment": c["content"],
                        "create_by": c["userid"],
                        "create_time": datetime.fromtimestamp(int(c["time"])),
                        "update_by": c["userid"],
                        "update_time": datetime.fromtimestamp(int(c["time"])),
                    }
                    comments.append(cc)
            cursor.executemany(sql, comments)
            cursor.close()
            conn.commit()
            TextPipeline.count += 1
        except Exception as e:
            print("数据库入库错误：", e)
            logging.error("数据库入库错误：", e)
            conn.close()

    def _delete_exists(self, connection, id):
        sql = "DELETE FROM cadrem_pubopinion_article WHERE id=%s "
        cursor = connection.cursor()
        result = cursor.execute(sql, id)
        sql = "DELETE FROM cadrem_pubopinion_comment WHERE article_id=%s"
        result2 = cursor.execute(sql, id)
        return result and result2
