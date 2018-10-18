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
        returnValue = json.loads(response._get_body().decode())["returnValue"]
        # for i in returnValue["datas"]:
        #     items = aliItem()
        #     items["name"] = i["name"]
        #     items["secondCategory"] = i["secondCategory"]
        #     items['workLocation'] = i['workLocation']
        #     items['recruitNumber'] = i['recruitNumber']
        #     items['gmtModified'] = i['gmtModified']
        #     items['description'] = i['description']
        #     items['requirement'] = i['requirement']
        #     items["href"] = 'https://job.alibaba.com/zhaopin/position_detail.htm?positionId={}'.format(i['id'])
            # yield scrapy.Request(
            #     items["href"],
            #     callback=self.parse_detail,
            #     meta={"items": items}
            # )
            # yield items
        if int(returnValue['pageIndex']) < int(returnValue['totalPage']):
            # print(returnValue['pageIndex'])
            pageIndex = int(returnValue['pageIndex']) + 1
            # print(pageIndex)
            pageSize = returnValue['pageSize']
            t = '%0.16f' % random.random()

            next_url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
            data = {'pageSize': str(pageSize), 't': str(t), 'pageIndex': pageIndex}
            # print(data)
    #         data= {
    #     "pageSize": "10",
    #     "t": "0.4459761467958639",
    #     "pageIndex": 3
    # }
            data = json.dumps(data).encode()
            print("body",data)
            #    b'{"pageIndex": 3, "t": "0.4459761467958639", "pageSize": "10"}'
            # data={"pageSize": "10","t": "0.4459761467958639","pageIndex": 3}
            yield scrapy.Request(next_url, callback=self.parse_next, method='POST', body=data, dont_filter=True)

    def parse_next(self, response):

        print(response.url)
        print(response.request.body)
        # print(response.body.decode())

        pageIndex = json.loads(response.body.decode())["returnValue"]['pageIndex']
        print(pageIndex)

        '''
        returnValue = json.loads(response.body.decode())["returnValue"]
        # print(returnValue)
        for i in returnValue["datas"]:
            items = aliItem()
            items["name"] = i["name"]
            items["secondCategory"] = i["secondCategory"]
            items['workLocation'] = i['workLocation']
            items['recruitNumber'] = i['recruitNumber']
            items['gmtModified'] = i['gmtModified']
            items['description'] = i['description']
            items['requirement'] = i['requirement']
            items["href"] = 'https://job.alibaba.com/zhaopin/position_detail.htm?positionId={}'.format(i['id'])
            yield scrapy.Request(
                items["href"],
                callback=self.parse_detail,
                meta={"items": items}
            )
        if returnValue['pageIndex'] < returnValue['totalPage']:
            # print(returnValue['pageIndex'])
            pageIndex = int(returnValue['pageIndex']) + 1
            print(pageIndex)
            # print(pageIndex)
            pageSize = returnValue['pageSize']
            t = '%0.16f' % random.random()
            next_url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
            #           https://job.alibaba.com/zhaopin/socialPositionList/doList.json
            data = {'pageSize': str(pageSize), 't': str(t), 'pageIndex': pageIndex}

            body = json.dumps(data)
            # print(pageIndex)
            print(data)
            yield scrapy.Request(next_url, callback=self.parse_next, method='POST', body=body)
        '''
    def parse_detail(self, response):
        pass
