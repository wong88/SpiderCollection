import json

import requests
from lxml import etree


class Game:
    def __init__(self):
        self.start_url = 'http://www.4399.com/flash'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Safari/537.36'
        }
        self.game_list = []

    def get_url(self, url):
        next_url = 'http://www.4399.com'
        next_url += url
        return next_url

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode('gb2312')

    def parse_response(self, response):
        html = etree.HTML(response)
        lis = html.xpath('//ul [@class="n-game cf"]/li')
        next_url_list = html.xpath('//a[text()="下一页"]/@href')[0] if len(html.xpath('//a[text()="下一页"]/@href'))>0 else None
        print(next_url_list)
        for li in lis:
            game = {}
            game['url'] = li.xpath('./a/@href')[0]
            game['name'] = li.xpath('.//b/text()')
            # game['pthot_url'] = li.xpath('./a/img/@src')
            game['sort'] = li.xpath('.//em[1]/a/text()')
            game['time'] = li.xpath('.//em[2]/text()')
            self.game_list.append(game)
        return next_url_list

    def save(self):
        with open('data/game.txt', 'a')as f:
            for g in self.game_list:
                json.dump(g, f, ensure_ascii=False, indent=2)

    def run(self):
        # 发送请求
        response = self.get_response(self.start_url)
        # 解析响应
        next_url_list = self.parse_response(response)
        # 保存数据
        self.save()
        while next_url_list is not None:
            next_url = self.get_url(next_url_list)
            # 发送请求
            response = self.get_response(next_url)
            # 解析响应
            next_url_list = self.parse_response(response)
            # 保存数据
            self.save()


if __name__ == '__main__':
    game = Game()
    game.run()
