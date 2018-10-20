# -*- coding: utf-8 -*-
import re

import scrapy
import json
from ..items import DiDi

class DidiSpider(scrapy.Spider):
    name = 'DiDi'
    allowed_domains = ['talent.didiglobal.com']
    start_urls = ['http://talent.didiglobal.com/recruit-portal-service/api/job/front/list?page=1&recruitType=1&size=16']

    def parse(self, response):
        result = json.loads(response.body.decode())
        data = result['data']
        total = data['total']
        page = data['page']
        size = data['size']
        items_list = data['items']
        print(items_list)
        print(len(items_list))
        for item in items_list:
            items = DiDi()
            items['jobName'] = item['jobName']
            items['refreshTime'] = item['refreshTime']
            items['workArea'] = item['workArea']
            items['deptName'] = item['deptName']
            jdId = item['jdId']
            detil_url = 'http://talent.didiglobal.com/recruit-portal-service/api/job/front/view/{}'.format(jdId)
            yield scrapy.Request(
                detil_url,
                meta={
                    'items':items
                },
                callback=self.parse_detil
            )
        if int(page)<int(total):
            next_url = 'http://talent.didiglobal.com/recruit-portal-service/api/job/front/list?page={}&recruitType=1&size={}'.format(page,size)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
    def parse_detil(self,response):
        items = response.meta['items']
        data = json.loads(response.body.decode())['data']
        items['recruitNum'] = data['recruitNum']
        items['jobDesc'] = re.sub(r'\n|\u2028', '',data['jobDesc'])
        items['qualification'] = re.sub(r'\n|\u2028', '',data['qualification'])
        yield items