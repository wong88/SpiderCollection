# -*- coding: utf-8 -*-

import scrapy
from ..items import RecruitmentItem


class TencentSpider(scrapy.Spider):
    name = "Tencent"
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=#a0']

    def parse(self, response):
        # 获取列表页
        tr_list = response.xpath("//table [@class='tablelist']/tr")[1:-1]
        for tr in tr_list:
            items = RecruitmentItem()
            items['position'] = tr.xpath(".//td[1]/a/text()").extract_first()
            items['href'] = tr.xpath(".//td[1]/a/@href").extract_first()
            items['category'] = tr.xpath(".//td[2]/text()").extract_first()
            items['num'] = tr.xpath(".//td[3]/text()").extract_first()
            items['location'] = tr.xpath(".//td[4]/text()").extract_first()
            items['time'] = tr.xpath(".//td[5]/text()").extract_first()
            detail_url= "https: // hr.tencent.com" + items["href"]
            yield scrapy.Request(
                detail_url,
                callback=self.parse_detail,
                meta={"items": items}
            )

        # 获取下一页
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url != "javascript:;":  # 判断是不是下一页
            # next_url = "https://hr.tencent.com/" + next_url
            # 通过urllib.parse.urljoin()进行url地址的拼接
            # next_url = urllib.parse.urljoin(response.url,next_url)
            # yield scrapy.Request(  #构造requests对象，通过yield叫个引擎
            #     next_url,
            #     callback=self.parse
            # )
            # 根据repsponse的url地址，对next_url进行url地址的拼接，构造请求
            yield response.follow(next_url, callback=self.parse)

    def parse_detail(self, response):
        items = response.meta["items"]
        items["responsibility"] = response.xpath("//ul [@class = 'squareli']/li/text()").extract()
        items["require"] = response.xpath("//ul [@class = 'squareli']/li/text()").extract()
        yield items
