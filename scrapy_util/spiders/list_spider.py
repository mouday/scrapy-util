# -*- coding: utf-8 -*-
import scrapy
from mo_cache import FileCache


class ListSpider(scrapy.Spider):
    """
    翻页爬虫基类，用于需要持续翻页的爬虫
    """
    # 记录的页码地址的key，用于需要持续翻页的爬虫
    page_key = None

    _cache = None

    # 翻页存储 set(key, value)/get(key)
    @property
    def cache(self):
        if not self._cache:
            self._cache = FileCache()

        return self._cache

    @property
    def _page_key(self):
        if self.page_key is None:
            raise Exception("page_key is None")
        else:
            return self.page_key

    def get_next_page(self):
        """
        从redis 中获取页码地址
        :return: int
        """

        page = self.cache.get(self._page_key)

        if not page:
            page = 1

        return page

    def set_next_page(self, page):
        """
        设置redis中的页码地址
        :param page: int/str
        :return:
        """

        self.cache.set(self._page_key, page)

    def parse(self, response):
        raise NotImplementedError()
