# -*- coding: utf-8 -*-
"""
@File    : spider_util.py
@Date    : 2024-04-15
"""
from scrapy import cmdline


def run_spider(spider):
    """
    运行爬虫
    @param spider: str / Spider
    @return: None
    """
    spider_name = None

    if isinstance(spider, str):
        spider_name = spider
    else:
        if hasattr(spider, 'name'):
            spider_name = getattr(spider, 'name')
        else:
            raise Exception('not spider_name')

    cmdline.execute(["scrapy", "crawl", spider_name])
