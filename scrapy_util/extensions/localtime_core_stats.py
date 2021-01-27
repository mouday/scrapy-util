# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy.extensions.corestats import CoreStats


class LocaltimeCoreStats(CoreStats):
    """使用本地时间统计"""
    def spider_opened(self, spider):
        self.stats.set_value('start_time', datetime.now(), spider=spider)

    def spider_closed(self, spider, reason):
        self.stats.set_value('finish_time', datetime.now(), spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)
