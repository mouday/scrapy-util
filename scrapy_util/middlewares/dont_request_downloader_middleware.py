# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse

from scrapy_util.logger import logger


class DontRequestDownloaderMiddleware(object):
    """不用网络请求的脚本，直接返回 Response"""

    def process_request(self, request, spider):
        logger.info('*' * 32)
        logger.info(self.__class__.__name__)
        logger.info('*' * 32)

        return HtmlResponse(url=request.url, request=request)
