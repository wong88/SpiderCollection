# -*- coding: utf-8 -*-
import re

import scrapy
import json
from ..items import BaiDu


class BaiduSpider(scrapy.Spider):
    name = 'BaiDu'
    allowed_domains = ['talent.baidu.com']
    start_urls = ['https://talent.baidu.com/baidu/web/httpservice/getPostList?recruitType=2&pageSize=10&curPage=1']

    def parse(self, response):
        result = json.loads(response.body.decode())
        currentPage = result['currentPage']
        totalPage = result['totalPage']
        pageSize = result['pageSize ']
        postList = result['postList']
        for post in postList:
            items = BaiDu()
            items['name'] = post['name']
            items['publishDate'] = post['publishDate']
            items['postType'] = post['postType']
            items['workPlace'] = post['workPlace']
            items['recruitNum'] = post['recruitNum']
            items['workContent'] = re.sub(r'<br>|\r', '',post['workContent'])
            items['serviceCondition'] = re.sub(r'<br>|\r', '',post['serviceCondition'])
            yield items
        if int(currentPage) < int(totalPage):
            next_url = 'https://talent.baidu.com/baidu/web/httpservice/getPostList?recruitType=2&pageSize={}&curPage={}'.format(pageSize,currentPage)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
