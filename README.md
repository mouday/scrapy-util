# Scrapy util

基于scrapy 的一些扩展

## 启用数据收集功能

此功能配合 [spider-admin-pro](https://github.com/mouday/spider-admin-pro) 使用

```python

# 设置收集运行日志的路径,会以post方式提交json数据
STATS_COLLECTION_URL = "http://127.0.0.1:5001/api/collection"

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