import time
import requests
import json


class TouTiao:
    def __init__(self):
        self.url = 'https://m.toutiao.com/list/?tag=__all__&ac=wap&count=20&format=json_raw&as=A1351B5B6EA96A1&cp=5BBED9C6AAD18E1&min_behot_time={}&_signature=rUb9LgAA9wYHab2uyxfCI61G.T&i={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        }

    def get_url(self):
        start_time = '%d' % time.time()
        time.sleep(0.1)
        end_time = '%d' % time.time()
        url = self.url.format(start_time, end_time)
        return url

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_response(self, response):
        response = json.loads(response)
        return response

    def save_response(self, response):
        with open('data/toutiao.txt', 'a')as f:
            json.dump(response, f, ensure_ascii=False, indent=2)

    def run(self):
        # 获取url
        url = self.get_url()
        # 发起请求获取响应
        response = self.get_response(url)
        # 处理响应获取我们想要的数据
        self.parse_response(response)
        # 保存数据
        self.save_response(response)


if __name__ == '__main__':
    toutiao = TouTiao()
    toutiao.run()
