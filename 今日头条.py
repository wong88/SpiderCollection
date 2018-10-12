import time
from queue import Queue
import threading
import requests
import json


class TouTiao:
    def __init__(self):
        self.url = 'https://m.toutiao.com/list/?tag=__all__&ac=wap&count=20&format=json_raw&as=A1351B5B6EA96A1&cp=5BBED9C6AAD18E1&min_behot_time={}&_signature=rUb9LgAA9wYHab2uyxfCI61G.T&i={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        }
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_list_queue = Queue()

    def get_url(self):
        for i in range(10):
            start_time = '%d' % time.time()
            end_time = '%d'%(time.time()+1)
            url = self.url.format(start_time, end_time)
            self.url_queue.put(url)


    def get_response(self):
        while True:
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers=self.headers)
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()
            print(4)
    def parse_response(self):
        while True:
            response = self.html_queue.get()
            parse_responses = json.loads(response)
            self.content_list_queue.put(parse_responses)
            self.html_queue.task_done()

    def save_response(self):
        while True:
            parse_responses = self.content_list_queue.get()
            print(1)
            with open('data/toutiao.txt', 'a')as f:
                json.dump(parse_responses, f, ensure_ascii=False, indent=2)
            print(2)
            self.content_list_queue.task_done()

    def run(self):
        threading_list = []
        # 获取url
        t_url = threading.Thread(target=self.get_url)
        threading_list.insert(0,t_url)
        # 发起请求获取响应
        t_get = threading.Thread(target=self.get_response)
        threading_list.insert(1,t_get)
        # 处理响应获取我们想要的数据
        t_parse = threading.Thread(target=self.parse_response)
        threading_list.insert(2,t_parse)
        # 保存数据
        t_save = threading.Thread(target=self.save_response)
        threading_list.insert(3,t_save)
        for t in threading_list:
            t.setDaemon(True)
            t.start()
        for q in [self.url_queue, self.html_queue, self.content_list_queue]:
            q.join()


if __name__ == '__main__':
    toutiao = TouTiao()
    toutiao.run()
