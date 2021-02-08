# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

import pymongo
from md5util import Md5Util
from scrapy.exceptions import DropItem
from scrapy_util.items import MongoItem
from scrapy_util.logger import logger


class MongoPipeline(object):
    """
    参考：
    https://doc.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb

    配置
    MONGO_URI
        eg: mongodb://localhost:27017/

    =====================================
    MongoItem      >   settings
    - - - - - - - - - - - - - - - - - -
    database       >   MONGO_DATABASE
    table          >   MONGO_TABLE
    data {dict}
    id_fields {list}

    """

    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, mongo_uri, mongo_database, mongo_table):
        self.mongo_uri = mongo_uri
        self.mongo_database = mongo_database
        self.mongo_table = mongo_table
        self.client = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_database=crawler.settings.get('MONGO_DATABASE', 'data'),
            mongo_table=crawler.settings.get('MONGO_TABLE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 类型控制
        if not isinstance(item, MongoItem):
            return item

        table = self.get_table(item)
        data = self.get_data(item)

        self.insert_data(table, data)

    def get_table(self, item):
        """item 自定义表名和库名优先于settings 配置"""
        mongo_database = item.get("database", self.mongo_database)
        mongo_table = item.get("table", self.mongo_table)

        return self.client[mongo_database][mongo_table]

    def insert_data(self, table, data):
        """插入数据"""
        try:
            result = table.insert(data)
            logger.info("success: {}".format(result))
        except (pymongo.errors.DuplicateKeyError, pymongo.errors.ServerSelectionTimeoutError) as e:
            logger.info("error: {}".format(e))
        finally:
            raise DropItem

    def get_datetime(self):
        """获取时间"""
        return datetime.now().strftime(self.DATE_TIME_FORMAT)

    def get_id(self, item):
        """获取id，用于去重"""
        data = item['data']

        if '_id' in data:
            return data['_id']

        elif 'id_fields' in item:
            id_fields = item["id_fields"]
            return Md5Util.get_data_md5(data, id_fields)

        else:
            return uuid.uuid4().hex

    def get_data(self, item):
        """处理数据"""
        data = item["data"]

        data['_id'] = self.get_id(item)
        data["create_time"] = self.get_datetime()

        return data
