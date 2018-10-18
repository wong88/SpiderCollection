# -*- coding: utf-8 -*-
import scrapy
import json
import random
import re

from ..items import aliItem

class AliSpider(scrapy.Spider):
    name = 'ali'
    allowed_domains = ['job.alibaba.com']
    start_urls = ['https://job.alibaba.com/zhaopin/socialPositionList/doList.json?pageSize=10&t=0.4005137021411369']

    def parse(self, response):
        returnValue = json.loads(response.body.decode())["returnValue"]
        for i in returnValue["datas"]:
            items = aliItem()
            items["name"] = i["name"]
            items["secondCategory"] = i["secondCategory"]
            items['workLocation'] = i['workLocation']
            items['recruitNumber'] = i['recruitNumber']
            items['gmtModified'] = i['gmtModified']
            items['description'] = re.sub(r'<br/>+|\s+|\t','',i['description'])
            items['requirement'] = re.sub(r'<br/>+|\s+|\t','',i['requirement'])
            items["href"] = 'https://job.alibaba.com/zhaopin/position_detail.htm?positionId={}'.format(i['id'])
            yield scrapy.Request(
                        items["href"],
                        callback=self.parse_detail,
                        meta={"items": items}
            )
        if int(returnValue['pageIndex']) < int(returnValue['totalPage']):
            pageIndex = int(returnValue['pageIndex']) + 1
            pageSize = returnValue['pageSize']
            t = '%0.16f' % random.random()
            next_url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
            data = {'pageSize': str(pageSize), 't': str(t), 'pageIndex': str(pageIndex)}
            yield scrapy.FormRequest(
                next_url,
                formdata=data,
                callback=self.parse_next
            )

    def parse_next(self, response):
        returnValue = json.loads(response.body.decode())["returnValue"]
        for i in returnValue["datas"]:
            items = aliItem()
            items["name"] = i["name"]
            items["secondCategory"] = i["secondCategory"]
            items['workLocation'] = i['workLocation']
            items['recruitNumber'] = i['recruitNumber']
            items['gmtModified'] = i['gmtModified']
            items['description'] = re.sub(r'<br/>+|\s+|\t', '', i['description'])
            items['requirement'] = re.sub(r'<br/>+|\s+|\t', '', i['requirement'])
            items["href"] = 'https://job.alibaba.com/zhaopin/position_detail.htm?positionId={}'.format(i['id'])
            yield scrapy.Request(
                items["href"],
                callback=self.parse_detail,
                meta={"items": items}
            )
        if returnValue['pageIndex'] < returnValue['totalPage']:
            pageIndex = int(returnValue['pageIndex']) + 1
            # print(pageIndex)
            pageSize = returnValue['pageSize']
            t = '%0.16f' % random.random()
            next_url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
            data = {'pageSize': str(pageSize), 't': str(t), 'pageIndex': str(pageIndex)}
            yield scrapy.FormRequest(
                next_url,
                formdata=data,
                callback=self.parse_next
            )

    def parse_detail(self, response):
        items = response.meta['items']
        items['put_time'] = response.xpath('//table[@class="detail-table box-border"]//tr[1]/td[2]/text()').extract_first().strip()
        items['term'] = response.xpath('//table[@class="detail-table box-border"]//tr[1]/td[6]/text()').extract_first().strip()
        items['department'] = response.xpath('//table[@class="detail-table box-border"]//tr[2]/td[2]/text()').extract_first().strip()
        items['education'] = response.xpath('//table[@class="detail-table box-border"]//tr[2]/td[4]/text()').extract_first().strip()
        yield items

