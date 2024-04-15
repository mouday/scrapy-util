# Scrapy util

基于scrapy 的一些扩展

pypi: [https://pypi.org/project/scrapy-util](https://pypi.org/project/scrapy-util)

github: [https://github.com/mouday/scrapy-util](https://github.com/mouday/scrapy-util)


```bash
pip install six scrapy-util
```

## 启用数据收集功能

此功能配合 [spider-admin-pro](https://github.com/mouday/spider-admin-pro) 使用

```python

# 设置收集运行日志的路径,会以post方式向 spider-admin-pro 提交json数据
# 注意：此处配置仅为示例，请设置为 spider-admin-pro 的真实路径
# 假设，我们的 spider-admin-pro 运行在http://127.0.0.1:5001
STATS_COLLECTION_URL = "http://127.0.0.1:5001/api/statsCollection/addItem"

# 启用数据收集扩展
EXTENSIONS = {
   # ===========================================
   # 可选：如果收集到的时间是utc时间，可以使用本地时间扩展收集
   'scrapy.extensions.corestats.CoreStats': None,
   'scrapy_util.extensions.LocaltimeCoreStats': 0,
   # ===========================================
   
   # 可选，打印程序运行时长
   'scrapy_util.extensions.ShowDurationExtension': 100,
   
   # 启用数据收集扩展
   'scrapy_util.extensions.StatsCollectorExtension': 100
}

```

## 使用脚本Spider

仅做脚本执行，Request 不请求网络

```python
# -*- coding: utf-8 -*-

from scrapy import cmdline

from scrapy_util.spiders import ScriptSpider


class BaiduScriptSpider(ScriptSpider):
    name = 'baidu_script'

    def execute(self):
        print("hi")


if __name__ == '__main__':
    cmdline.execute('scrapy crawl baidu_script'.split())

```

## 列表爬虫

ListNextRequestSpider基于 ListSpider 实现，如需自定义缓存，可以重写其中的方法

```python
# -*- coding: utf-8 -*-

from scrapy import cmdline
from scrapy_util.spiders import ListNextRequestSpider


class BaiduListSpider(ListNextRequestSpider):
    name = 'list_spider'

    page_key = "list_spider"
    
    # 必须实现的方法
    def get_url(self, page):
        return 'http://127.0.0.1:5000/list?page=' + str(page)

    def parse(self, response):
        print(response.text)
        
        # 调用下一页，该方法会在start_requests 方法自动调用一次
        # 如果不继续翻页，可以不调用
        yield self.next_request(response)


if __name__ == '__main__':
    cmdline.execute('scrapy crawl list_spider'.split())

```

## MongoDB中间件

使用示例

settings.py
```python
# 1、设置MongoDB 的数据库地址
MONGO_URI = "mongodb://localhost:27017/"

# 2、启用中间件MongoPipeline
ITEM_PIPELINES = {
   'scrapy_util.pipelines.MongoPipeline': 100,
}

```

```python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import cmdline
from scrapy_util.items import MongoItem


class BaiduMongoSpider(scrapy.Spider):
    name = 'baidu_mongo'

    start_urls = ['http://baidu.com/']
    
    # 1、设置数据库的表名
    custom_settings = {
        'MONGO_DATABASE': 'data',
        'MONGO_TABLE': 'table'
    }

    def parse(self, response):
        title = response.css('title::text').extract_first()

        item = {
            'data': {
                'title': title
            }
        }
        
        # 2、返回 MongoItem
        return MongoItem(item)


if __name__ == '__main__':
    cmdline.execute('scrapy crawl baidu_mongo'.split())

```
 
如果需要做微调，可以继承`MongoPipeline` 重写函数


## 工具方法

运行爬虫工具方法

```python
import scrapy
from scrapy_util import spider_util

class BaiduSpider(scrapy.Spider):
    name = 'baidu_spider'


if __name__ == '__main__':
    # cmdline.execute('scrapy crawl baidu_spider'.split()
    spider_util.run_spider(BaiduSpider)
```

