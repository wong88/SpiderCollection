import requests
from lxml import etree
import re


def url_manager():
    """url管理"""
    url_new = "https://movie.douban.com/top250"
    if url_new_list:
        url_next = url_new_list.pop()
        url_new = "https://movie.douban.com/top250%s" % url_next
        url_old_list.add(url_new)
        print(url_new)
    return url_new


def html_download(url):
    """HTML下载"""
    html = requests.get(url).content.decode('utf-8')
    return html


def html_parser(html):
    """HTML解析"""
    ha = ""
    movie = ""
    selector = etree.HTML(html)
    # 电影名称
    title = selector.xpath('//div [@class="hd"]/a/span[1]/text()')
    # 电影相关信息
    bodys = re.findall(r'<p class="">\s+(.*)<br>\s+(.*)', html)
    # for i in bodys:
    #     body =
    # 评分
    start = selector.xpath('//div [@class="bd"]/div /span [@class= "rating_num"]/text()')
    # 电影评价人数
    comment_num = selector.xpath('//div [@class="bd"]/div /span[4]/text()')
    # 让人记忆深刻的一句话
    # rhesis = selector.xpath('//div div [@class="bd"]/p [@class="quote"]/span/')
    # 获取新的url
    url_next = selector.xpath('//div [@class="paginator"]/span [@class="next"]/link [@rel="next"]/@href')
    for i in range(0, len(title)):
        movie += "电影名称:%s  电影信息:%s%s   电影评分:%s    评价人数:%s \n" % (
        title[i],re.sub(r"(&nbsp;|\.\.\.|\/)"," ",bodys[i][0]), re.sub(r"(&nbsp;|\.\.\.|\/)"," ",bodys[i][1]), start[i], comment_num[i])
    if not url_next:
        return movie, None
    return movie, url_next[0]


def dataoutput(movie):
    """解析数据存储"""
    with open("data/豆瓣电影top250.txt", 'a')as f:
        f.write(movie)


def crawl():
    """调用爬虫"""
    # 爬虫入口
    url = "https://movie.douban.com/top250"
    html = html_download(url)
    movie,url_next = html_parser(html)
    dataoutput(movie)
    if url_next == None:
        dataoutput(movie)
        print("下载完毕")
    while url_next:
        url_new_list.add(url_next)
        url = url_manager()
        html = html_download(url)
        movie, url_next = html_parser(html)
        url_new_list.add(url_next)
        dataoutput(movie)


if __name__ == '__main__':
    url_new_list = set()
    url_old_list = set()
    crawl()
