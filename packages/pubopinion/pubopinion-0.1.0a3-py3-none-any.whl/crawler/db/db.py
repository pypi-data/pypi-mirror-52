# -*- coding: utf-8 -*-
# filename: db.py
import threading
from collections import namedtuple

import math
import pymysql
import logging
from crawler.db.db_config import ENABLED_DB
from crawler.db.db_config import DB_CONFIG


class DatabaseConfigParser:

    logger = logging.getLogger("DatabaseConfigParser")

    def __init__(self, db_configs):
        if db_configs is None:
            raise BaseException("参数db_configs不能为空")

        self.db_configs = db_configs

    def get_config(self, config_name):
        logger = DatabaseConfigParser.logger
        configs = self.db_configs

        if config_name is None:
            logger.debug("config_name is None.")
            return

        for config in configs:
            if "name" in config.keys() and config["name"] == config_name:
                return config

        return


class DatabaseConfiguration(dict):
    logger = logging.getLogger("DatabaseConfiguration")

    def __init__(self, seq=None, **kwargs):
        self["ENABLED_DB"] = ENABLED_DB
        self.parser = DatabaseConfigParser(DB_CONFIG)
        self.__parse()

    def __parse(self):
        db_name = self["ENABLED_DB"]

        if db_name is None:
            self.logger.error("数据库配置错误，ENABLED_DB 为空")
            raise BaseException("database config exception, ENABLED_DB is None!")

        config = self.parser.get_config(db_name)

        if config is None:
            self.logger.error("数据库配置不存在！请检查DB_CONFIG配置项")
        else:
            for k in config:
                self[k] = config[k]


class MySqlHelper(object):

    logger = logging.getLogger("MySqlHelper")

    def __init__(self, db_config=None):
        self.config = DatabaseConfiguration() if not db_config else db_config
        self.conn = self.__connect_db()
        if "pool_size" not in self.config.keys() or type(self.config["pool_size"]) != "int":
            self.pool_size = 5
        else:
            self.pool_size = self.config["pool_size"]
        self.pool = []
        # 初始化线程池
        for i in range(self.pool_size):
            self.pool.append(self.__connect_db())

    def __is_connect(self):
        self.logger.debug("数据库连接中……")
        config = self.config

        if not config:
            self.logger.debug("获取数据库配置失败！")
        conn = pymysql.connect(config["hostname"], config["username"],
                               config["password"])

        if conn is None:
            self.logger.error("数据库连接失败！")
            return False

        if config["database"] is None:
            self.logger.error("数据库名不可为空。")
            return False

        # 创建数据库
        cursor = conn.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS `%s` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;" \
              % config["database"]
        cursor.execute(sql)
        cursor.close()
        conn.close()
        return True

    def __connect_db(self):
        config = self.config
        if self.__is_connect():
            return pymysql.connect(config["hostname"], config["username"],
                                   config["password"], config["database"])

    def get_one(self, sql, param=None):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, param)
        data = cursor.fetchone()
        cursor.close()
        self.__release(conn)
        return data

    def get_all(self, sql, param=None):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, param)
        data = cursor.fetchall()
        cursor.close()
        self.__release(conn)
        return data

    def get_dict(self, sql, param=None):
        return self.get_all(sql, param)

    def __release(self, conn):
        if conn is not None:
            self.pool.append(conn)

    def __get_connection(self):
        conn = None
        while conn is None:
            if len(self.pool) > 0:
                conn = self.pool.pop()
        return conn

    def insert(self, sql, data=None):
        conn = self.__get_connection()
        cursor = conn.cursor()
        row_count = cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        self.__release(conn)
        return row_count

    def insert_many(self, sql, data=None):
        conn = self.__get_connection()
        cursor = conn.cursor()
        row_count = cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        self.__release(conn)
        return row_count

    def delete(self, sql, param=None):
        conn = self.__get_connection()
        cursor = conn.cursor()
        row_count = cursor.execute(sql, param)
        conn.commit()
        cursor.close()
        self.__release(conn)
        return row_count

    def update(self, sql, param=None):
        conn = self.__get_connection()
        cursor = conn.cursor()
        row_count = cursor.execute(sql, param)
        conn.commit()
        cursor.close()
        self.__release(conn)
        return row_count

    def execute_batch(self, sql, param=None):
        conn = self.__get_connection()
        cursor = conn.cursor()
        row_count = cursor.executemany(sql, param)
        conn.commit()
        cursor.close()
        self.__release(conn)
        return row_count

    def close(self):
        pool_size = self.pool_size
        while pool_size > 0:
            conn = self.__get_connection()
            pool_size -= 1
            conn.close()


class SingleMySqlPool(MySqlHelper):
    count = 0
    self = None
    lock = threading.Lock()

    @staticmethod
    def get_instance():
        lock = SingleMySqlPool.lock
        if SingleMySqlPool.self is None:
            lock.acquire()
            if SingleMySqlPool.self is None:
                SingleMySqlPool.self = SingleMySqlPool()
            lock.release()
        lock.acquire()
        SingleMySqlPool.count += 1
        lock.release()
        return SingleMySqlPool.self

    def close(self):
        lock = SingleMySqlPool.lock
        lock.acquire()
        SingleMySqlPool.count -= 1
        lock.release()
        if SingleMySqlPool.count == 0:
            super().close()


def get_connection():
    config = {
        "name": "test",
        "hostname": "localhost",
        "username": "root",
        "password": "123",
        "database": "public_opinion_test0",
        "pool_size": 5
    }
    conn = pymysql.connect(config["hostname"], config["username"],
                           config["password"], config["database"])
    return conn


class StorageDAO(object):

    MAX_LIMIT = 2147483648

    def __init__(self):
        pass

    def insert(self):
        conn = get_connection()
        cursor = conn.cursor()
        # cursor.execute(query="")
        cursor.close()
        conn.commit()
        conn.close()

    def select(self, offset=0, limit=MAX_LIMIT):
        conn = get_connection()
        cursor = conn.cursor()
        args = {
            "offset": offset,
            "limit": limit,
        }
        cursor.execute("SELECT * FROM `text` LIMIT %(offset)s, %(limit)s", args)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def select_named(self, offset=0, limit=MAX_LIMIT):
        result = self.select(offset, limit)
        if len(result) < 0:
            return result
        HTMLEntity = namedtuple("HTMLEntity", ["url", "text"])
        result_set = []
        for record in result:
            e = HTMLEntity(*record)
            result_set.append(e)
        return result_set
