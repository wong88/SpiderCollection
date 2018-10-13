from parse_url import parse_url
import json


class Zhihu:
    def __init__(self):
        self.url = 'https://www.zhihu.com/api/v3/explore/guest/feeds?limit=15'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }

    def run(self):
        while True:
            response = parse_url(self.url, self.headers)
            response_dict = self.parse_response(response)
            self.download(response_dict)
            print('已下载15条热点')

    def parse_response(self, response):
        response_dict = json.loads(response)
        return response_dict

    def download(self,response_dict):
        with open('知乎热点.txt','a',encoding='utf-8') as f:
            json.dump(response_dict,f,ensure_ascii=False,indent=2)

if __name__ == '__main__':
    zhihu = Zhihu()
    zhihu.run()
