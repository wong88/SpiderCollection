from queue import Queue
import requests
import json
import threading

class DouYu:
    def __init__(self):
        self.url = 'https://www.douyu.com/gapi/rkc/directory/0_0/{}'
        self.headers = {
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Safari/537.36'
        }
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_list_queue = Queue()
    def get_url(self):
        for i in range(127):
            url = self.url.format(i)
            print(url)
            self.url_queue.put(url)

    def get_response(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url,headers = self.headers)
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()

    def parse_response(self):
        while True:
            response = self.html_queue.get()
            response_dict = json.loads(response)
            self.content_list_queue.put(response_dict)
            self.html_queue.task_done()

    def save(self):
        i = 1
        while True:
            response_dict = self.content_list_queue.get()
            with open('data/douyu.txt','a')as f:
                json.dump(response_dict,f,ensure_ascii=False,indent=2)
                print(i)
                i+=1
                self.content_list_queue.task_done()
    def run(self):
        threading_list = []
        # 获取url
        t_url = threading.Thread(target=self.get_url)
        threading_list.append(t_url)
        # 发起请求获取响应
        for i in range(3):
            t_get = threading.Thread(target=self.get_response)
            threading_list.append(t_get)
        # 获取响应中的数据
        t_parse = threading.Thread(target=self.parse_response)
        threading_list.append(t_parse)
        # 保存处理后的响应
        for i in range(3):
            t_save = threading.Thread(target=self.save)
            threading_list.append(t_save)
        for t in threading_list:
            t.setDaemon(True)
            t.start()
        for q in [self.url_queue,self.html_queue,self.content_list_queue]:
            q.join()

if __name__ == '__main__':
    douyu = DouYu()
    douyu.run()
