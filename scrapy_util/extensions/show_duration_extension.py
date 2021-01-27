# -*- coding: utf-8 -*-

# @Date    : 2018-12-12
# @Author  : Peng Shiyu

from scrapy import signals

from scrapy_util.logger import logger


class ShowDurationExtension(object):
    """
    打印持续时间
    """

    def __init__(self, crawler):
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def spider_closed(self, spider, reason):
        stats = spider.crawler.stats.get_stats()

        # 获取数据
        item_scraped_count = stats.get("item_scraped_count", 0)
        item_dropped_count = stats.get("item_dropped_count", 0)

        start_time = stats.get("start_time")
        finish_time = stats.get("finish_time")

        # 打印收集日志
        item_count = item_scraped_count + item_dropped_count
        duration = (finish_time - start_time).seconds

        logger.info("*" * 30)
        logger.info("* {}".format(spider.name))
        logger.info("* item_count : {}".format(item_count))
        logger.info("* duration : {}".format(duration))
        logger.info("*" * 30)
