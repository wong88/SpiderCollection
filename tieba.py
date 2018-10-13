from lxml import etree
import sys
import json
import re
from queue import Queue

from parse_url import parse_url


class TieBa:
    def __init__(self, baname):
        # 起始url
        self.url = 'http://jump.bdimg.com/mo/q----,sz@320_240-1-3---/m?kw={}&amp;lp=7202'.format(baname)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
            'Referer': 'http://jump.bdimg.com/f?ie=utf-8&kw=%E6%9F%AF%E5%8D%97&pn=0&',
        }
        # 列表页爬取页数
        self.start_page = 1
        # 起始总页数
        self.page = 2
        # 详情页等页面头url,用于拼接url
        self.pares_url = 'http://jump.bdimg.com/mo/q----,sz@320_240-1-3---/'

        # self.url_queue = Queue()
        # self.html_queue = Queue(maxsize=10)
        # self.content_list_queue = Queue()

    def parse_response(self, response):
        # 帖子名
        title_list = []
        # 帖子url
        content_url_list = []
        # 帖子详情
        information_list = []
        # 解析列表页帖子信息
        selector = etree.HTML(response)
        # 下一页url地址
        next_page_url_list = selector.xpath('//a[text()="下一页"]/@href') if selector.xpath('//a[text()="下一页"]/@href') else None
        # 总页数
        page_max = re.findall('&*#*1*6*0*;*第[1-9]+/(.*?)页', response) if re.findall('&#160;第.*?/(.*?)页',response) else [1]
        # 分组
        divs = selector.xpath("//div[contains(@class,'i')]")
        for div in divs:
            # 帖子名称
            title_list.extend(div.xpath('./a/text()'))
            # 帖子url
            content_url_list.extend(div.xpath('./a/@href'))
            # 帖子的信息:发帖人等信息
            information_list.extend(div.xpath('./p/text()'))
        return title_list, content_url_list, information_list, next_page_url_list, page_max

    def get_tie_content(self, content_url, i):
        # 获取详情页信息
        p = int(i) * 30
        # 拼接详情页分页url
        url = self.pares_url + content_url + '&pn=' + str(p)
        # 获取详情页数据
        tie_response = parse_url(url, self.headers)
        # 处理详情页数据
        tie_response = re.sub('encoding="UTF-8"', ' ', tie_response)
        return tie_response

    def parse_tie_content(self, tie_response):
        # 解析详情页信息
        # print(type(tie_response))
        tie_content = []
        author = []
        photo_url = []
        information = []
        reply_count = []

        html = etree.HTML(tie_response)
        # 帖子详情页下一页url
        tie_next_page_url_list = html.xpath('//a[text()="下一页"]/@href') if html.xpath('//a[text()="下一页"]/@href') else None
        # 帖子详情页总页数
        tie_page_max = re.findall('&#160;第.*?/(.*?)页', tie_response)[0] if re.findall('&#160;第1/(.*?)页',tie_response) else 0
        # 分组
        divs = html.xpath('//div [@class = "i"]')
        for div in divs:
            # 帖子楼层
            tie_content.append(str(div.xpath('./text()')))
            # 帖子作者
            author.extend(div.xpath('.//span[@class="g"]/a/text()'))
            # 帖子中照片url
            photo_url.append(str(div.xpath('.//img[@class = "BDE_Image"]/@src')) if div.xpath(
                './/img[@class = "Bphoto_urlphoto_urlDE_Image"]/@src') else [])
            # 发帖时间
            information.extend(div.xpath('.//span[@class="b"]/text()'))
            # 帖子评论rul
            reply_count.append(self.pares_url + div.xpath('.//td [@class ="r"]/a/@href')[0] if div.xpath(
                './/td [@class ="r"]/a/href|.//td [@class ="r"]/a/text()') else [])
        return tie_content, author, photo_url, information, reply_count, tie_next_page_url_list, tie_page_max

    def save_tie_reply(self, title, tie_content, author, photo_url, information, reply_count, ):
        # 保存帖子详情页信息
        for i in range(len(tie_content)):
            tie_reply = {}
            tie_reply[title] = {author[i]:
                                    [tie_content[i],
                                     information[i],
                                     {'photo_url': photo_url[i]},
                                     {'comment_url': reply_count[i]}]}
            try:
                with open('data/%s.txt' % title, 'a', encoding='utf-8') as f:
                    json.dump(tie_reply, f, ensure_ascii=False, indent=2)
            except:
                pass
    def run(self):
        while self.start_page < self.page:
            # 发送请求,获取响应
            response = parse_url(self.url, self.headers)
            # 处理响应结果
            response = re.sub('encoding="UTF-8"', '', response)
            # 解析响应结果
            title_list, content_url_list, information_list, next_page_url_list, page_max = self.parse_response(response)
            # 获得总页数
            self.page = int(page_max[0])
            for i in range(len(title_list)):
                # 发送请求获取帖子详情页数据
                tie_response = self.get_tie_content(content_url_list[i], 0)
                # 获取详情页数据
                tie_content, author, photo_url, information, reply_count, tie_next_page_url_list, tie_page_max = self.parse_tie_content(
                    tie_response)
                # 保存数据
                self.save_tie_reply(title_list[i], tie_content, author, photo_url, information, reply_count)
                print('帖子第1页以爬完')
                p = 1
                pp = 2
                # 获取详情页后面的数据
                while p < tie_page_max:
                    tie_response = self.get_tie_content(content_url_list[i], p)
                    tie_content, author, photo_url, information, reply_count, tie_next_page_url_list, page_max = self.parse_tie_content(
                        tie_response)
                    print('帖子第%d页以爬完' % pp)
                    pp += 1
                    p += 1
                    self.save_tie_reply(title_list[i], tie_content, author, photo_url, information, reply_count)

            self.url = 'http://jump.bdimg.com/mo/q----,sz@320_240-1-3---/m?kw=%E6%9F%AF%E5%8D%97&amp;lp=7202'
            self.url += next_page_url_list[0]
            print('第%d页爬完' % self.start_page)
            self.start_page += 1


if __name__ == '__main__':
    # baname = input("请输入想爬取的贴吧名")
    # baname = sys.argv[1]
    baname = '柯南'
    tieba = TieBa(baname)
    tieba.run()
