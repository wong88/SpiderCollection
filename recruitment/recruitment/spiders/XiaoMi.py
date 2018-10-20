# -*- coding: utf-8 -*-
import re

import scrapy
import json
from ..items import XiaoMi


class XiaomiSpider(scrapy.Spider):
    name = 'XiaoMi'
    allowed_domains = ['job.hr.xiaomi.com']
    start_urls = ['http://job.hr.xiaomi.com/api/apply/jobs?limit=10&offset=0&&siteId=287&orgId=xiaomi']

    def __init__(self):
        super()
        self.page = 10
        self.total = 0

    def parse(self, response):
        jobs_information = json.loads(response.body.decode())
        self.total = jobs_information['jobStats']['total']
        jobs_list = jobs_information['jobs']
        for jobs in jobs_list:
            items = XiaoMi()
            items['title'] = jobs['title']
            items['publishedAt'] = jobs['publishedAt']
            items['name'] = jobs['department']['name']
            items['id'] = jobs['id']
            detil_url = 'http://job.hr.xiaomi.com/api/apply/job/{}?orgId=xiaomi&siteId=287'
            yield   scrapy.Request(
                detil_url,
                meta={
                    'items': items
                },
                callback=self.parse_detil
            )
        next_url = 'http://job.hr.xiaomi.com/api/apply/jobs?limit=10&offset={}&&siteId=287&orgId=xiaomi'.format(str(self.page))
        if self.page < self.total:
            self.page += 10
            yield scrapy.Request(
                next_url,
                callback=self.parse_next
            )

    def parse_detil(self, response):
        items = response.meta['items']
        detil_information = json.loads(response.body.decode())
        items['jobDescription'] = re.sub(r'<p>|</p>|<br>', '', detil_information['jobDescription'])
        yield   items

    def parse_next(self, response):
        jobs_information = json.loads(response.body.decode())
        jobs_list = jobs_information['jobs']
        for jobs in jobs_list:
            items = XiaoMi()
            items['title'] = jobs['title']
            items['publishedAt'] = jobs['publishedAt']
            items['name'] = jobs['department']['name']
            items['id'] = jobs['id']
            detil_url = 'http://job.hr.xiaomi.com/api/apply/job/{}?orgId=xiaomi&siteId=287'
            yield   scrapy.Request(
                detil_url,
                meta={
                    'items': items
                },
                callback=self.parse_detil
            )
        next_url = 'http://job.hr.xiaomi.com/api/apply/jobs?limit=10&offset={}&&siteId=287&orgId=xiaomi'.format(str(self.page))
        if self.page < self.total:
            self.page += 10
            yield scrapy.Request(
                next_url,
                callback=self.parse_next
            )
