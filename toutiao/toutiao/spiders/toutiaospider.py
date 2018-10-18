# -*- coding: utf-8 -*-
import scrapy


class ToutiaospiderSpider(scrapy.Spider):
    name = 'toutiaospider'
    allowed_domains = ['www.toutiao.com']
    start_urls = ['https://www.toutiao.com/']
    def parse(self, response):
        print(response)