# -*- coding: utf-8 -*-
import re

import scrapy
import json
import time

from ..items import HuaWei
class HuaweiSpider(scrapy.Spider):
    name = 'HuaWei'
    allowed_domains = ['career.huawei.com']
    start_urls = ['http://career.huawei.com/socRecruitment/services/portal3/portalnew/getJobList/page/15/1?keywords=']

    def parse(self, response):
        result = json.loads(response.body.decode())
        curPage = result['pageVO']['curPage']
        totalPages = result['pageVO']['totalPages']
        result_list = result['result']
        for temp in result_list:
            items = HuaWei()
            items['jobname'] = temp['jobname']
            items['jobArea'] = temp['jobArea']
            items['jobFamilyName'] = temp['jobFamilyName']
            items['deptName'] = temp['deptName']
            items['mainBusiness'] = re.sub(r'\n','',temp['mainBusiness'])
            jobId = temp['jobId']
            now_time = time.time()*1000
            detile_url = 'http://career.huawei.com/socRecruitment/services/portal/portalpub/getJobDetail?jobId={}&_={}'.format(jobId,now_time)
            yield scrapy.Request(
                detile_url,
                meta={
                    "items":items
                },
                callback=self.parse_detile
            )
        if curPage<totalPages:
            next_url = 'http://career.huawei.com/socRecruitment/services/portal3/portalnew/getJobList/page/15/{}?keywords='.format(str(curPage+1))
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
    def parse_detile(self,response):
        items = response.meta['items']
        result = json.loads(response.body.decode())
        items['jobRequire'] = re.sub(r'\n','',result['jobRequire'])
        yield items