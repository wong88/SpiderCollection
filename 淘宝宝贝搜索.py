from parse_url import parse_url
from pprint import pprint
import re
import json


class Taobao:
    def __init__(self,search):
        self.url = 'https://s.m.taobao.com/search?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&q='+seach+'&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=16&wlsort=16&page=1'
        self.headers = {
            'cookie': 'miid=8496424541985164793; t=4a270f6969886e3a1acf6997b6d8ec37; thw=cn; cna=GkyxE5EAXV4CAXE5ts2ZaS4Q; hng=CN%7Czh-CN%7CCNY%7C156; uc3=vt3=F8dBzrVLed%2Ft2JIQwcs%3D&id2=UoYZbjWaAUzT1w%3D%3D&nk2=2VqKUKaPAjPjMXP4ldU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=%5Cu80E1%5Cu5C0F%5Cu4EAE%5Cu5927%5Cu7231%5Cu67EF%5Cu5357; lgc=%5Cu80E1%5Cu5C0F%5Cu4EAE%5Cu5927%5Cu7231%5Cu67EF%5Cu5357; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; enc=7jZYigfnTp3Kck6frbLv0x56v8G3pweqasUoyTdtKoR5yjzAbsTRbY%2FR8UXzjGMT6pIuFRGbpnYlXm%2BJfGO%2FDg%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; ali_ab=183.95.51.195.1538900232054.8; cookie2=5f56813e599fffebe97f398d9c460b86; v=0; _tb_token_=7835ea93db356; mt=ci=-1_0; uc1=cookie14=UoTfItCn9ktIBQ%3D%3D; _m_h5_tk=88290c9d424efb00c17e99061c1f36e5_1539011825264; _m_h5_tk_enc=3568758f52ba5d562a2e7eb81f6a1be8; JSESSIONID=5A44A58AEBD59BB0C7684AEBABEE2F13; isg=BGhoxtcxp7ANpIvs_TFEe89YOVa6Oduxoe1SjyKZtOPWfQjnyqGcK_67cVMoyYRz',
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
