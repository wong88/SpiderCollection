# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

client = MongoClient()


class RecruitmentPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'Tencent':
            collection = client["tencent"]["hr"]
            print('tencent:%s'%dict(item))
            collection.insert_one(dict(item))
        elif spider.name == 'ali':
            collection = client["ali"]["hr"]
            # print(item['pageIndex'])
            print('ali:%s'%dict(item))
            collection.insert_one(dict(item))
        elif spider.name =='bytedance':
            collection = client['bytedance']['hr']
            print('bytedance:%s'%dict(item))
            collection.insert_one(dict(item))