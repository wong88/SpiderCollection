# -*- coding: utf-8 -*-
import scrapy
from ..items import EcPriceItem
from selenium import webdriver
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['search.jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=macbook pro 15 2018 16 256']
    def __init__(self):
        super()
        self.page = 1
        self.browser = webdriver.Chrome()
    def parse(self, response):
        url_title = 'https:'
        page = str(self.page+1)
        sku_list = []
        li_list = response.xpath("//ul[@class = 'gl-warp clearfix']/li")
        for li in li_list:
            items = EcPriceItem()
            items['price'] = li.xpath(".//div[@class='p-price']//i/text()").extract_first()
            items['goods_name'] = li.xpath(".//div[@class = 'p-name p-name-type-2']/a/em/text()|.//div[@class = 'p-name p-name-type-2']/a/em/font[@class='skcolor_ljg']/text()").extract()
            items['goods_url'] = url_title+li.xpath(".//div[@class = 'p-name p-name-type-2']/a/@href").extract_first()
            items['commit_url'] = url_title+li.xpath(".//div[@class = 'p-commit']/strong/a/@href").extract_first()
            items['commit_count'] = li.xpath(".//div[@class = 'p-commit']/strong/a/text()").extract_first()
            items['shop_name'] = li.xpath(".//div[@class='p-shop']//a/text()").extract_first()
            items['shop_url'] = url_title+li.xpath(".//div[@class='p-shop']//a/@href").extract_first()
            sku = li.xpath("./@data-sku").extract_first()
            sku_list.append(sku)

