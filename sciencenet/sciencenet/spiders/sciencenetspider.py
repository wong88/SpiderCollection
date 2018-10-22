# -*- coding: utf-8 -*-
from urllib.parse import quote
from scrapy import Request
import scrapy
import requests

from sciencenet.sciencenet.items import SciencenetItem


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
            print(url)
            start_request = Request(url=url, callback=self.parse)
            start_request.headers["Referer"] = "http://blog.sciencenet.cn/blog.php"
            yield start_request

    def parse(self, response):
        items = SciencenetItem()
