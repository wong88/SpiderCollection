from parse_url import parse_url
from pprint import pprint
import re
import json


class Taobao:
    def __init__(self,search):
        self.url = 'https://s.m.taobao.com/search?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&q='+seach+'&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=16&wlsort=16&page=1'
        self.headers = {
            'referer': 'https://s.m.taobao.com/h5?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&sst=1&n=20&buying=buyitnow&q=%E6%B8%94%E5%A4%AB%E5%B8%BD',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }
        self.search =search
    def get_url(self, page):
        self.url = 'https://s.m.taobao.com/search?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&q=渔夫帽&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=16&wlsort=16&page=' + str(page)

    def run(self):
        response_str = parse_url(self.url, self.headers)
        response_dict, total_page = self.parse_content(response_str)
        self.download(response_dict)
        print('第1页爬取完毕')
        page = 1
        while page < int(total_page):
            self.get_url(page)
            response_str = parse_url(self.url, self.headers)
            response_dict, total_page = self.parse_content(response_str)
            self.download(response_dict)
            page += 1
            print('第%d页爬取完毕'%page)

    def parse_content(self, response_str):
        response_str = re.sub(r'[(|)]', '', response_str)
        response_dict = json.loads(response_str)
        total_page = response_dict['totalPage']
        return response_dict, total_page

    def download(self, response_dict):
        with open('%s.txt'%self.search, 'a', encoding='utf-8') as f:
            json.dump(response_dict, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    seach = input('请输入您想搜索的内容')
    taobao = Taobao(seach)
    taobao.run()
