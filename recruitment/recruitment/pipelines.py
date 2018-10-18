# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

client = MongoClient()
collection = client["tencent"]["hr"]


class RecruitmentPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        collection.insert_one(dict(item))
        return item
