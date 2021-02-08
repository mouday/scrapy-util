# -*- coding: utf-8 -*-

from scrapy import Spider

from scrapy_util.items.trick_item import TrickItem


class ScriptSpider(Spider):
    """继承该类，用于仅做脚本执行，Request 不请求网络"""
    start_urls = ['https://www.baidu.com/']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            # 脚本直接返回，不进行网络请求 Middleware
            'scrapy_util.middlewares.DontRequestDownloaderMiddleware': 100,

            # 取消不使用的Middleware，加快运行速度
            'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
            'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': None,
            'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
            'scrapy.downloadermiddlewares.stats.DownloaderStats': None
        }
    }

    def parse(self, response):
        self.execute()
        return TrickItem()

    def execute(self):
        raise NotImplementedError()
