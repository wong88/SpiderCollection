# http://wh.ganji.com/fang1/m0o2/
import requests
from pymongo import MongoClient
from lxml import etree
from retrying import retry
from queue import Queue


class GanJi:
    def __init__(self):
        self.url = 'http://wh.ganji.com/fang1/m0o{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Safari/537.36'
        }
        Client = MongoClient()
        self.collection = Client['daili']['kuai']
        self.proxies = {
            'http': 'http://107.151.152:21880'
        }
        self.proxies_queue = Queue()

    def get_url(self):
        pass

    def get_proxies(self):
        proxies_list = self.collection.find()
        for proxies in proxies_list:
            proxies = {
                'http': proxies['ip']
            }
            self.proxies_queue.put(proxies)

    @retry(stop_max_attempt_number=3)
    def get_response(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=3, proxies=self.proxies)
            if '请输入验证码' in response.content.decode():
                print(1,response.status_code)
                raise None
            if response.status_code != 200:
                print(response.status_code)
                print(0,response.status_code)
                raise 0
        except:
            self.proxies = self.proxies_queue.get()
            print(self.proxies)
            self.get_response()
        else:
            return response.content.decode()

    def perse_response(self, response):
        html = etree.HTML(response)
        div_list = html.xpath("//div[@class = 'f-list js-tips-list']/div")[1:]
        print(len(div_list))
        next_url = html.xpath("//a[@class='next']/span/text()")
        print(next_url)

    def run(self):
        self.get_proxies()
        # 发送请求,获取响应
        response = self.get_response()
        # 解析响应
        self.perse_response(response)
        # 保存数据


if __name__ == '__main__':
    ganji = GanJi()
    ganji.run()
