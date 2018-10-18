# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitmentItem(scrapy.Item):
    # define the fields for your item here like:
    position = scrapy.Field()  # 职位名称
    href = scrapy.Field()  # 职位url
    category = scrapy.Field()  # 职位类别
    num = scrapy.Field()  # 人数
    location = scrapy.Field()  # 地址
    time = scrapy.Field()  # 发布时间
    responsibility = scrapy.Field()  # 工作职责
    require = scrapy.Field()  # 工作要求


class aliItem(scrapy.Item):
    name = scrapy.Field()
    secondCategory = scrapy.Field()
    workLocation = scrapy.Field()
    recruitNumber = scrapy.Field()
    gmtModified = scrapy.Field()
    description = scrapy.Field()
    requirement = scrapy.Field()
    href = scrapy.Field()
    put_time = scrapy.Field()
    term = scrapy.Field()
    department = scrapy.Field()
    education = scrapy.Field()
    pageIndex = scrapy.Field()

class bytedance(scrapy.Item):
    name = scrapy.Field()
    summary = scrapy.Field()
    city = scrapy.Field()
    create_time = scrapy.Field()
    description = scrapy.Field()
    requirement = scrapy.Field()