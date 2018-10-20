# -*- coding: utf-8 -*-
import json
import re

from ..items import JD
import scrapy


class JdSpider(scrapy.Spider):
    name = "JD"
    allowed_domains = ["zhaopin.jd.com"]
    start_urls = (
        'http://zhaopin.jd.com/web/job/job_info_list/3',
    )
    pageIndex = 1
    # def __init__(self):
    #     super()

    #     self.pageIndex = 1
    def parse(self, response):
        yield scrapy.FormRequest(
            'http://zhaopin.jd.com/web/job/job_list',
            formdata={
                'pageIndex': str(self.pageIndex),
                'pageSize': '10'
                    },
            callback=self.parse_post
        )
    def parse_post(self,response):
        job_list = json.loads(response.body.decode())

        for job in job_list:
            items = JD()
            items['positionName'] = job['positionName']
            items['jobType'] = job['jobType']
            items['workCity'] = job['workCity']
            items['formatPublishTime'] = job['formatPublishTime']
            items['workContent'] = re.sub(r'\r\n','',job['workContent'])
            items['qualification'] = re.sub(r'\r\n','',job['qualification'])
            yield items
        yield scrapy.FormRequest(
        'http://zhaopin.jd.com/web/job/job_list',
        formdata={
            'pageIndex': str(self.pageIndex+1),
            'pageSize': '10'
                },
        callback=self.parse_post)