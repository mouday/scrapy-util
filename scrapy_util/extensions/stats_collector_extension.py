# -*- coding: utf-8 -*-

# @Date    : 2018-12-12
# @Author  : Peng Shiyu

import requests
from scrapy import signals

from scrapy_util.logger import logger
import os

class StatsCollectorExtension(object):
    """
    日志记录扩展
    """
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, crawler, log_file=None, stats_collection_url=None):
        self.stats_collection_url = stats_collection_url
        self.log_file = log_file

        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        log_file = crawler.settings.get("LOG_FILE")
        stats_collection_url = crawler.settings.get("STATS_COLLECTION_URL")

        if stats_collection_url is None:
            raise Exception('STATS_COLLECTION_URL not in settings')

        return cls(crawler, log_file=log_file, stats_collection_url=stats_collection_url)

    def spider_closed(self, spider, reason):
        stats = spider.crawler.stats.get_stats()

        # 获取数据
        start_time = stats.get("start_time")
        finish_time = stats.get("finish_time")
        duration = (finish_time - start_time).seconds
        # 保存收集到的信息
        item = {
            "job_id": os.environ.get("SCRAPYD_JOB",""),
            "project": os.environ.get("SCRAPY_PROJECT",""),
            "spider": spider.name,
            "item_scraped_count": stats.get("item_scraped_count", 0),
            "item_dropped_count": stats.get("item_dropped_count", 0),
            "start_time": start_time.strftime(self.DATETIME_FORMAT),
            "finish_time": finish_time.strftime(self.DATETIME_FORMAT),
            "duration": duration,
            "finish_reason": stats.get("finish_reason"),
            "log_error_count": stats.get("log_count/ERROR", 0),
        }

        logger.info(item)

        self.collection_item(item)

    def collection_item(self, item):
        """处理收集到的数据,以json 形式提交"""
        res = requests.post(self.stats_collection_url, json=item)
        logger.info(res.text)

