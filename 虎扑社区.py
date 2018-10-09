from lxml import etree

from parse_url import parse_url


class Hupu:
    def __init__(self):
        self.url = 'https://m.hupu.com/bbs/34'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }

    def parse_response(self, response):
        selector = etree.HTML(response)
        rule = '//div [2]/ul/li/a/@href'
        news_url_list = selector.xpath(rule)
        rule = '//div [2]/ul/li/a/div/div/h3/text()'
        title_list = selector.xpath(rule)
        rule = '//div [2]/ul/li/a/div/div/div/div/text()'
        auther_list = selector.xpath(rule)
        return news_url_list, title_list, auther_list

    def run(self):
        response = parse_url(self.url, self.headers)
        news_url_list, title_list, auther_list = self.parse_response(response)
        for i in range(0,len(news_url_list)):
            print(news_url_list[i],title_list[i])


if __name__ == '__main__':
    hupu = Hupu()
    hupu.run()
