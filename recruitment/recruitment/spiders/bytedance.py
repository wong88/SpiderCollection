# -*- coding: utf-8 -*-
import json
import re

import scrapy

from ..items import bytedance


class BytedanceSpider(scrapy.Spider):
    name = "bytedance"
    allowed_domains = ["job.bytedance.com"]
    start_urls = (
        'https://job.bytedance.com/api/recruitment/position/campus_list/?limit=10&offset=',
    )

    def parse(self, response):
        # print(response.request.url)
        data_dict = json.loads(response.body.decode())
        data_list = data_dict['positions']
        count = data_dict['count']
        for datas in data_list:
            items = bytedance()
            items['name'] = datas['name']
            items['summary'] = datas['summary']
            items['city'] = datas['city']
            items['create_time'] = datas['create_time']
            items['description'] = re.sub(r'<br/>+|\s+|\t','',datas['description'])
            items['requirement'] = re.sub(r'<br/>+|\s+|\t','',datas['requirement'])
            yield items
        for i in range(0, count, 10):
            url = 'https://job.bytedance.com/api/recruitment/position/campus_list/?limit=10&offset=' + str(i)
            yield scrapy.Request(
                url,
                callback=self.parse,
            )