# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from collections import OrderedDict


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class DoubanItemPipeline():

    def __init__(self):
        self.file_name = "highlightsD.json"
        self.handler = open(self.file_name, 'w')

    def process_item(self, item, spider):
        self.handler.write(json.dumps(dict(item)) + '\n')

        return item

    def close_spider(self, spider):
        self.handler.close()


class RautahakuPipeline(object):

    def open_spider(self, spider):
        self.items = {"data": []}
        # self.file = null  # open('items.json', 'w')

    def close_spider(self, spider):
        self.file = open('highlights.json', 'w')
        self.file.write(json.dumps(self.items))
        self.file.close()

    def process_item(self, item, spider):
        self.items["data"].append(dict(item))
        return item
