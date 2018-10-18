# -*- coding: utf-8 -*-
import scrapy
import json
import random
from ..items import aliItem
class AliSpider(scrapy.Spider):
    name = 'ali'
    allowed_domains = ['job.alibaba.com']
    start_urls = ['https://job.alibaba.com/zhaopin/socialPositionList/doList.json?pageSize=10&t=0.4005137021411369']

    def parse(self, response):
        # print(dict(response))
        returnValue = json.loads(response._get_body().decode())["returnValue"]
        for i in returnValue["datas"]:
            items = aliItem()
            items["name"] = i["name"]
            items["secondCategory"] = i["secondCategory"]
            items['workLocation'] = i['workLocation']
            items['recruitNumber'] = i['recruitNumber']
            items['gmtModified'] = i['gmtModified']
            items['description'] = i['description']
            items['requirement'] = i['requirement']
            items["href"] ='https://job.alibaba.com/zhaopin/position_detail.htm?positionId={}'.format(i['id'])
            # print("*"*100)
            # yield scrapy.Request(
            #     items["href"],
            #     callback = self.parse_detail,
            #     meta = {"items":items}
            # )
            yield items
        if returnValue['pageIndex']<returnValue['totalPage']:
            pageIndex = int(returnValue['pageIndex'])+1
            pageSize = returnValue['pageSize']
            t ='%0.8f'%random.random()
            next_url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
            data = {'pageSize': pageSize,'t': str(t),'pageIndex':str(pageIndex)}
            yield response.follow(next_url, callback=self.parse, method='POST', body=data)


    def parse_detail(self, response):
        pass
