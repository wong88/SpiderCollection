from parse_url import parse_url
import json
from get_classify import get_classify


class Douban:
    def __init__(self):
        self.url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?os=android&start=0&count=18&loc_id=108288'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Mobile Safari/537.36',
            'Referer': 'https://m.douban.com/tv/american'
        }
        self.classify_url = 'https://m.douban.com/tv/'

    def get_url(self, classify, i=0):
        self.url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_' + classify + '_hot/items?os=android&start=' + str(
            i) + '&count=18&loc_id=108288'

    def run(self):
        classify_list, original_list = get_classify(self.classify_url, self.headers)
        print(classify_list)
        for classify in classify_list:
            print('开始爬取%s分类的数据' % classify)
            self.get_url(classify)
            print(self.url)
            response_str = parse_url(self.url, self.headers)
            response_dict, total = self.parse_content(response_str)
            self.download(response_dict)
            print("第1页爬完..")
            i = 18

            while i < total:
                self.get_url(classify, i)
                response_str = parse_url(self.url, self.headers)
                response_dict, total = self.parse_content(response_str)
                self.download(response_dict)
                i += 18
                j = i / 18
                print("第%d页爬完" % j)

    def parse_content(self, response_str):
        response_dict = json.loads(response_str)
        total = response_dict['total']
        return response_dict, total

    def download(self, response_dict):
        with open('data/douban.txt', 'a', encoding='utf-8') as f:
            json.dump(response_dict, f, ensure_ascii=False,indent=2)



if __name__ == '__main__':
    douban = Douban()
    douban.run()
