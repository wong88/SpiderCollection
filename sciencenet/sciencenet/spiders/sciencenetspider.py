# -*- coding: utf-8 -*-
import re
from urllib.parse import quote
from scrapy import Request
import scrapy
from lxml import etree
from copy import deepcopy

from ..items import SciencenetItem


class SciencenetspiderSpider(scrapy.Spider):
    name = "sciencenetspider"
    allowed_domains = ["blog.sciencenet.cn"]
    host_url = "http://blog.sciencenet.cn/"
    base_url = "http://blog.sciencenet.cn/blog.php?mod=member&type="
    blog_base_url = "http://blog.sciencenet.cn/home.php?mod=space&uid="
    blogger_base_url = "http://blog.sciencenet.cn/blog.php?mod=member&type={}&realmmedium={}&realm={}&catid={}"

    realm_list = ["生命科学", "医学科学", "化学科学", "工程材料", "信息科学", "地球科学", "数理科学", "管理综合"]

    def start_requests(self):
        # 通过一级学科构造起始url列表
        for realm in self.realm_list:
            url = self.base_url + quote(realm, encoding="gbk")
            # print(url)
            start_request = Request(url=url, callback=self.parse)
            start_request.headers["Referer"] = "http://blog.sciencenet.cn/blog.php"
            yield start_request

    def parse(self, response):
        # 获取一级学科
        request_url = response.request.url
        first = re.findall('type=(.*)', request_url)[0]
        # print("request_url:%s"%request_url)
        # 获取二级学科
        div_list = response.xpath("//div[@id='con_box']/div")
        # 通过二级学科获取三级学科
        for div in div_list:
            items = SciencenetItem()
            items['second_name'] = div.xpath("./div[@class = 'box_l']/text()").extract_first()
            li_list = div.xpath("./div[@class='box_r']/ul/li")
            for li in li_list:
                items['thirdly_name'] = li.xpath("./a/text()").extract_first()
                thirdly_url = li.xpath("./a/@href").extract_first()
                catid = re.findall('&catid=(.*)',thirdly_url)[0]
                items['thirdly_url'] = "http://blog.sciencenet.cn/blog.php?mod=member&type={}&realmmedium={}&realm={}&catid={}".format(quote(items['thirdly_name'], encoding="gbk"),quote(items['second_name'], encoding="gbk"),first,catid)
                yield scrapy.Request(
                    items['thirdly_url'],
                    meta={
                        'items':deepcopy(items)
                    },
                    callback=self.parse_usrs_list
                )
    def parse_usrs_list(self,response):
        items = response.meta['items']
        html = response.body.decode("gbk")
        response = etree.HTML(html)
        div_list = response.xpath("//div[@class='potbox']")
        for div in div_list:
            # 'http://blog.sciencenet.cn/' +
            items['user_url'] = 'http://blog.sciencenet.cn/'+div.xpath("./div[@class = 'pot']/a/@href")[0]
            items['user_name'] = div.xpath("p[@class = 'potfont']/a/text()")[0]
            yield scrapy.Request(
                items['user_url'],
                meta={
                    'items':deepcopy(items)
                },
                callback=self.parse_detil

            )
    def parse_detil(self,response):
        items = response.meta['items']
        html = response.body.decode("gbk")
        response = etree.HTML(html)
        items['orientation'] = response.xpath("//li[@class='ul_diy']//text()")[0]   if len(response.xpath("//li[@class='ul_diy']//text()"))>0 else []
        items['Visits'] = response.xpath("//strong[@class='xi1']/text()")[0]    if len(response.xpath("//strong[@class='xi1']/text()"))>0 else []
        items['count'] = response.xpath("//li[text()='博文: ']/a/text()")   if len(response.xpath("//li[text()='博文: ']/a/text()"))>0 else []
        items['vitality'] = response.xpath("//li[text()='活跃度: ']/a/text()")  if len(response.xpath("//li[text()='活跃度: ']/a/text()"))>0 else []
        yield items
