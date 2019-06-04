# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class TextPipeline(object):
    """
    筛选数据
    """
    def __init__(self):
        self.limit = 30

    def process_item(self, item, spider):
        """
        Spider生成的item会传递进来
        """
        if item['text']:
            if len(item['text']) > self.limit:
                # 省略超出的内容
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem("Missing Text")

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        # 数据库连接信息
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        获取配置信息
        """
        return cls(
            # 通过crawler获取全局配置的配置信息
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
    
    def open_spider(self, spider):
        """
        Spider开启时，方法被调用
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
        数据存储至MongoDB
        """
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item
        
    def close_spider(self, spider):
        """
        Spider关闭时，方法被调用
        """ 
        self.client.close()

