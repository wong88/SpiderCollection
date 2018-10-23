# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SciencenetItem(scrapy.Item):
    # define the fields for your item here like:
    thirdly_name = scrapy.Field()   # 二级分类名字
    second_name =scrapy.Field()     # 三级分类名字
    thirdly_url = scrapy.Field()    # 三级分类url
    user_url = scrapy.Field()       # 用户url
    user_name = scrapy.Field()      # 用户名
    orientation = scrapy.Field()    # 用户的方向
    Visits = scrapy.Field()         # 访问量
    count = scrapy.Field()          # 博文量
    vitality = scrapy.Field()       # 活跃度