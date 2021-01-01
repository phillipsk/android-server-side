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

    def __init__(self, images_store):
        self.images_store = images_store
        self.file_name = os.path.join(images_store, str(int(time.time())) + '.txt')
        self.handler = open(self.file_name, 'w')

    def process_item(self, item, spider):
        self.handler.write(json.dumps(dict(item)) + '\n')

        return item

    def close_spider(self, spider):
        self.handler.close()