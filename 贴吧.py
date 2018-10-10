from lxml import etree

import json
import re

from parse_url import parse_url


class TieBa:
    def __init__(self):
        self.url = 'http://jump.bdimg.com/mo/q----,sz@320_240-1-3---/m?kw=%E6%9F%AF%E5%8D%97&amp;lp=7202'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
            'Referer': 'http://jump.bdimg.com/f?ie=utf-8&kw=%E6%9F%AF%E5%8D%97&pn=0&',
        }
        self.start_page = 1
        self.page = 2

    def parse_response(self, response):
        selector = etree.HTML(response.encode())
        title_list = selector.xpath('//div [@class="i"]/a/text()|'
                                    '//div [@class="i x"]/a/text()')
        content_url_list = selector.xpath('//div [@class="i"]/a/@href|'
                                          '//div [@class="i x"]/a/@href')
        information_list = selector.xpath('//div [@class="i"]/p/text()|'
                                          '//div [@class="i x"]/p/text()')
        # for i in information:
        #     information = re.sub('\\[a-z][0-9]]','',i)
        # 存入字典,后续太麻烦
        # for i in range(0, len(title) - 1):
        #     tie[title[i]] = {content_url[i]: information[i]}
        next_page_url_list = selector.xpath('//a[text()="下一页"]/@href')
        page_list = selector.xpath('//input [@name="pnum"]/@value')
        return title_list, content_url_list, information_list, next_page_url_list, page_list

    def get_tie_content(self, content_url, i):
        p = int(i) * 30
        self.url = 'http://jump.bdimg.com/mo/q----,sz@320_240-1-3---/'
        url = self.url + content_url + '&pn=' + str(p)
        print(url)
        tie_response = parse_url(url, self.headers)
        return tie_response

    def parse_tie_content(self, tie_response):
        tie_reply_content_text_list = []
        tie_reply_content_photo_list = []
        tie_reply_auther_list = []
        tie_reply_count_list = []
        tie_reply_time_list = []
        tie_reply_content_all = re.findall(r'<div class="i">(.*?)<table><tr><td class="l">', tie_response)
        page_all = re.findall(r'<br/>第\d+/(.*?)页', tie_response)
        with open('data/tieba.txt', 'w', encoding='utf-8')as f:
            f.write(str(tie_reply_content_all))
        if page_all == []:
            page_all = [0]
        for i in range(len(tie_reply_content_all)):
            '''<div class="i">40楼. 我想说，我去年的奖品都还没有收到<br/><table><tr><td class="l">'''
            tie_reply_content_photo_list = (re.findall(r'<a href="(.*\.jpg)">', tie_reply_content_all[i]))
            tie_reply_auther_list = (re.findall(r'<span class="g"><.*?>(.*?)<.*?></span>', tie_response))
            tie_reply_count_list = (re.findall(r'<a href="(.*?)".*?class="reply_to">(.*?)</a>', tie_response))
            tie_reply_time_list = (re.findall(r'<span class="b">(.*?)</span>', tie_response))
            if len(tie_reply_count_list) < len(tie_reply_auther_list):
                tie_reply_count_list.insert(0, None)
            if len(tie_reply_content_photo_list) < len(tie_reply_auther_list):
                for i in range(len(tie_reply_auther_list) - len(tie_reply_content_photo_list)):
                    tie_reply_content_photo_list.insert(i, None)
                    # print(len(tie_reply_content_all))
                    # print(len(tie_reply_content_all))
                    # print(len(tie_reply_auther_list))
                    # print(len(tie_reply_count_list))
                    # print(len(tie_reply_time_list))
        return int(page_all[
                       0]), tie_reply_content_all, tie_reply_content_all, tie_reply_auther_list, tie_reply_count_list, tie_reply_time_list

    def save_tie(self, title_list, content_url_list, information_list):
        for i in range(len(title_list)):
            tie = {}
            tie[title_list[i]] = {content_url_list[i]: information_list[i]}
            with open('data/%s.txt' % title_list[i], 'w', encoding='utf-8') as f:
                json.dump(tie, f, ensure_ascii=False, indent=2)

    def save_tie_reply(self, title_list, tie_reply_content_text_list, tie_reply_content_photo_list,
                       tie_reply_auther_list, tie_reply_count_list, tie_reply_time_list):
        for i in range(len(tie_reply_content_text_list)):
            tie_reply = {}
            tie_reply[tie_reply_content_text_list[i]] = {
                str(tie_reply_auther_list[i]): [str(tie_reply_count_list[i]), str(tie_reply_time_list[i]),
                                                str(tie_reply_content_photo_list[i])]}
            with open('data/%s.txt' % title_list, 'a', encoding='utf-8') as f:
                json.dump(tie_reply, f, ensure_ascii=False, indent=2)

    def run(self):
        while self.start_page < self.page:
            response = parse_url(self.url, self.headers)
            response = re.sub('&#160;', ' ', response)
            title_list, content_url_list, information_list, next_page_url_list, page_list = self.parse_response(response)
            self.save_tie(title_list, content_url_list, information_list)
            for i in range(len(title_list)):
                tie_response = self.get_tie_content(content_url_list[i], 0)
                page_all, tie_reply_content_text_list, tie_reply_content_photo_list, tie_reply_auther_list, tie_reply_count_list, tie_reply_time_list = self.parse_tie_content(
                    tie_response)
                self.save_tie_reply(title_list[i], tie_reply_content_text_list, tie_reply_content_photo_list,
                                    tie_reply_auther_list, tie_reply_count_list, tie_reply_time_list)
                print('帖子第1页以爬完')
                p = 1
                pp = 2
                while p < page_all:
                    tie_response = self.get_tie_content(content_url_list[i], p)
                    page_all, tie_reply_content_text_list, tie_reply_content_photo_list, tie_reply_auther_list, tie_reply_count_list, tie_reply_time_list = self.parse_tie_content(
                        tie_response)
                    print('帖子第%d页以爬完' % pp)
                    pp += 1
                    p += 1
                    self.save_tie_reply(title_list[i], tie_reply_content_text_list,
                                        tie_reply_content_photo_list, tie_reply_auther_list, tie_reply_count_list,
                                        tie_reply_time_list)
            self.page = int(page_list[0])
            self.url = 'http://jump.bdimg.com/mo/q----,sz@320_240-1-3---/m?kw=%E6%9F%AF%E5%8D%97&amp;lp=7202'
            self.url += next_page_url_list[0]
            print('第%d页爬完' % self.start_page)
            self.start_page += 1


if __name__ == '__main__':
    tieba = TieBa()
    tieba.run()
