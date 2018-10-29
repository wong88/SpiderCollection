from multiprocessing.dummy import Pool
from lxml import etree
from queue import Queue
import requests
import threading
import re, json
from pymongo import MongoClient
from hashlib import sha1


class Jianshu:
    def __init__(self):
        self.start_url = 'https://www.jianshu.com/?page={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Safari/537.36'
        }
        self.pool = Pool(5)  # 默认大小是cup的个数
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.distinct_queue = Queue()
        self.content_list_queue = Queue()
        client = MongoClient()
        self.collection = client['jianshu']['data']
        self.lenth = 0
        self.llq = set()

    def get_url(self):
        for i in range(100):
            url = self.start_url.format(str(i))
            print(url)
            self.url_queue.put(url)

    def get_response(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()

    def parse_response(self):
        while True:
            response = self.html_queue.get()
            html = etree.HTML(response)
            uls = html.xpath('//ul[@class="note-list"]/li')
            for ul in uls:
                content = {}
                content["title"] = ul.xpath('.//a[@class = "title"]/text()')[0]
                content["content_url"] = ul.xpath('.//a[@class = "title"]/@href')[0] if len(
                    ul.xpath('.//a[@class = "title"]/@href')) > 1 else ' '
                content["photo_url"] = ul.xpath('./a/img/@src')[0] if len(ul.xpath('./a/img/@src')) > 1 else ' '
                content["simpleness_contrnt"] = re.sub(r'\n|\s', '', ul.xpath(".//p [@class = 'abstract']/text()")[0])
                content["auhtor"] = ul.xpath(".//a[@class = 'nickname']/text()")[0]
                content["author_url"] = ul.xpath('.//a[@class = "nickname"]/@href')[0]
                content["comment_url"] = ul.xpath('.//div[@class = "meta"]/a/@href')[0]
                content["comment"] = ul.xpath('.//div[@class = "meta"]/a/text()')[0]
                content["like"] = ul.xpath('.//div[@class = "meta"]/span[1]/text()')[0]
                content["Reward"] = ul.xpath('.//div[@class = "meta"]/span[2]/text()')[0] if len(
                    ul.xpath('.//div[@class = "meta"]/span[2]/text()')) > 1 else ' '
                # content_list.append(content)
                self.content_list_queue.put(content)
            self.html_queue.task_done()

    def distinct(self):
        while True:
            content = self.content_list_queue.get()
            sha = sha1()
            sha.update(json.dumps(content).encode())
            f = sha.hexdigest()
            self.llq.add(f)
            self.distinct_queue.put(content)
            self.content_list_queue.task_done()

    def save_response(self):
        while True:
            content = self.distinct_queue.get()
            self.lenth = len(self.llq)
            if len(self.llq) > self.lenth:
                self.collection.insert_one(content)
                self.content_list_queue.task_done()
                self.lenth = len(self.llq)
            else:
                print("重复信息: >>", json.dumps(content, ensure_ascii=False))
            self.distinct_queue.task_done()

    def run(self):
        threading_list = []
        # 获取url
        t_url = threading.Thread(target=self.get_url)
        threading_list.insert(0, t_url)
        # 发起请求获取响应
        t_get = threading.Thread(target=self.get_response)
        threading_list.insert(1, t_get)
        # 处理响应获取我们想要的数据
        t_parse = threading.Thread(target=self.parse_response)
        threading_list.insert(2, t_parse)
        # 保存数据
        t_save = threading.Thread(target=self.save_response)
        threading_list.insert(3, t_save)
        t_disdistinct = threading.Thread(target=self.distinct)
        threading_list.insert(4, t_disdistinct)
        for t in threading_list:
            t.setDaemon(True)
            t.start()
        for q in [self.url_queue, self.html_queue, self.content_list_queue]:
            q.join()


if __name__ == '__main__':
    jianshu = Jianshu()
    jianshu.run()
