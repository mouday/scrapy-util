# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy_util.spiders import ListSpider


class ListNextRequestSpider(ListSpider):
    """
    翻页爬虫扩展，用于需要持续翻页的爬虫
    """

    def get_url(self, page):
        raise NotImplementedError

    def next_request(self, response=None):
        if response:
            next_page = response.meta['page'] + 1
            self.set_next_page(next_page)

        page = self.get_next_page()
        url = self.get_url(page=page)
        return Request(url=url, meta={'page': page})

    def start_requests(self):
        yield self.next_request()
