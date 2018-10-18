import requests
from lxml import etree
from pymongo import MongoClient
import time
from retrying import retry


class Kuai:
    def __init__(self):
        self.start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Safari/537.36'
        }
        Client = MongoClient()
        self.collection = Client['daili']['kuai']

    def get_url(self):
        '''获取url'''
        url_list = []
        for i in range(1, 9999999):
            url_list.append(self.start_url.format(str(i)))
        return url_list

    def get_response(self, url):
        '''获取response'''
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_response(self, response):
        # 获取selector对象
        selector = etree.HTML(response)
        # 分组
        tr_list = selector.xpath("//table [@class = 'table table-bordered table-striped']/tbody/tr")
        daili_list = []
        for tr in tr_list:
            daili = {}
            ip = tr.xpath("./td[1]/text()")[0]
            daili['port'] = tr.xpath("./td[2]/text()")[0]
            http = tr.xpath("./td[4]/text()")[0]
            proxies = http + '://' + ip + ':' + daili['port']
            daili['ip'] = proxies

            # print(proxies)
            daili_list.append(daili)
        return daili_list

    # @retry(stop_max_attempt_number=3)
    def filter(self, daili_list):
        new_daili_list = []
        for daili in daili_list:
            proxies = {
                daili['port']:daili['ip']
            }
            print(proxies)
            time.sleep(0.5)
            try:
                response1 = requests.get("http://www.baidu.com", timeout=3,proxies=proxies)
                response2 = requests.get("https://gitee.com/moqsien",timeout=3,proxies=proxies)
                content1 = response1.content.decode()
                content2 = response2.content.decode()
                if 'nginx/' in (content1 or content2):
                    print(0)
                    raise 0
                elif (response1.status_code or response2.status_code) > 220:
                    print(response1.status_code)
                    print(response2.status_code)
                    raise 1
            except:
                print('验证失败:%s' % daili['ip'])
            else:
                print('验证通过daili:%s' % daili['ip'])
                new_daili_list.append(daili)

        return new_daili_list

    def save(self, daili_list):
        for daili in daili_list:
            print(daili)
            self.collection.insert_one(daili)

    def run(self):
        # 获取url
        url_list = self.get_url()
        for url in url_list:
            print(url)
            # 发起请求,获取响应
            response = self.get_response(url)
            # 解析响应,获取数据
            daili_list = self.parse_response(response)
            # 保存数据
            daili_list = self.filter(daili_list)
            self.save(daili_list)


if __name__ == '__main__':
    kuai = Kuai()
    kuai.run()
