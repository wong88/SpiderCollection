import time
from lxml import etree

from parse_url import parse_url

'''//li/div[@class="list_bd list_bd_3 list_link"]/@data-link|' \
               '//li/div[@class="list_bd list_bd_3 list_link"]/h3/text()|' \
               '//li/div[@class="list_bd list_bd_3 list_link"]/p/text()|' \
               '//li/div[@class="list_fun flex-hb-vc"]/div/span[1]/text()|' \
               '//li/div[@class="list_fun flex-hb-vc"]/div/span[2]/text()'''


class TianYa:
    def __init__(self):
        self.url = 'http://www.tianya.cn/m/find/bagua/index.shtml?_={}'
        self.headers = self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }

    def get_url(self):
        timeing = time.time() * 1000
        self.url = 'http://www.tianya.cn/m/find/bagua/index.shtml?_={}'.format(timeing)

    def parse_response(self, response):
        selector = etree.HTML(response)
        rule = '//li/div[@class="list_bd list_bd_3 list_link"]/@data-link'
        content_url_list = selector.xpath(rule)
        selector.xpath(rule)
        rule = '//li/div[@class="list_bd list_bd_3 list_link"]/h3/text()'
        title_list = selector.xpath(rule)
        rule = '//li/div[@class="list_bd list_bd_3 list_link"]/p/text()'
        subheading_list = selector.xpath(rule)
        rule = '//li/div[@class="list_fun flex-hb-vc"]/div/span/text()'
        auther_list = selector.xpath(rule)
        rule = '//li/div[@class="list_fun flex-hb-vc"]/span/text()'
        classify_list = selector.xpath(rule)
        return content_url_list, title_list, subheading_list, auther_list, classify_list

    def run(self):
        self.get_url()
        response = parse_url(self.url, self.headers)
        content_url_list, title_list, subheading_list, auther_list, classify_list = self.parse_response(response)


if __name__ == '__main__':
    tianya = TianYa()
    tianya.run()
