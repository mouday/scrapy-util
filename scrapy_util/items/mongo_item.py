# -*- coding: utf-8 -*-
from scrapy import Item, Field


class MongoItem(Item):
    """通用的MongoDB 数据 Item"""

    # 去重的字段组合list, 用于生成：_id
    id_fields = Field()

    # 数据
    data = Field()

    # 表配置信息
    database = Field()
    table = Field()
