# -*- coding: utf-8 -*-
import scrapy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['search.suning.com']
    start_urls = ['https://search.suning.com/']

    def start_requests(self):
        goods = input("请输入您需要的商品")
        for url in self.start_urls:
            url = url+goods+"/"
            print(url)
            yield self.make_requests_from_url(url)
    def parse(self, response):
        # TODO 价格获取
        pass
        # url = parameter,sugGoodsCode,sugGoodsCode,sugGoodsCode,cityCode,districtCode,shopCode,shopCode,shopCode,shopCode
""" https://icps.suning.com/icps-web/getVarnishAllPrice014/000000000690128134,000000000690128156,000000000690128135,000000000690128157_027_0270101_0000000000,0000000000,0000000000,0000000000_1_getClusterPrice.vhtm?callback=getClusterPrice"""