# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EcPriceItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    goods_name = scrapy.Field()
    goods_url = scrapy.Field()
    commit_url = scrapy.Field()
    commit_count = scrapy.Field()
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
    data_sku = scrapy.Field()

