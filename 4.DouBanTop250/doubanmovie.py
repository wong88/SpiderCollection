import requests
from lxml import etree
import re


def url_manager():
    """url管理"""
    # 初始地址
    url_new = "https://movie.douban.com/top250"
    # 判断是否重复
    if url_new_list:
        # 重复删除
        url_next = url_new_list.pop()
        # 构造下一页url地址
        url_new = "https://movie.douban.com/top250%s" % url_next
        #将地址加入老地址列表
        url_old_list.add(url_new)
        print(url_new)
    # 返回新地址
    return url_new


def html_download(url):
    """HTML下载"""
    # 发起请求,获取响应
    html = requests.get(url).content.decode('utf-8')
    return html


def html_parser(html):
    """HTML解析"""
    ha = ""
    movie = ""
    selector = etree.HTML(html)
    # 电影名称
    title = selector.xpath('//div [@class="hd"]/a/span[1]/text()')
    print(title)
    # 电影相关信息
    bodys = re.findall(r'<p class="">\s+(.*)<br>\s+(.*)', html)
    # 评分
    start = selector.xpath('//div [@class="bd"]/div /span [@class= "rating_num"]/text()')
    # 电影评价人数
    comment_num = selector.xpath('//div [@class="bd"]/div /span[4]/text()')
    # 让人记忆深刻的一句话
    rhesis = selector.xpath('//div [@class="bd"]/p [@class="quote"]/span/text()') if len(selector.xpath('//div [@class="bd"]/p [@class="quote"]/span/text()'))>0 else None
    print(rhesis)
    # 获取新的url
    url_next = selector.xpath('//div [@class="paginator"]/span [@class="next"]/link [@rel="next"]/@href')
    for i in range(0, len(title)):
        movie += "电影名称:%s  电影信息:%s%s   电影评分:%s    评价人数:%s  让人记忆深刻的一句话:%s \n" % (
        title[i],re.sub(r"(&nbsp;|\.\.\.|\/)"," ",bodys[i][0]), re.sub(r"(&nbsp;|\.\.\.|\/)"," ",bodys[i][1]), start[i], comment_num[i],rhesis[i])
    if not url_next:
        return movie, None
    return movie, url_next[0]


def dataoutput(movie):
    """数据存储"""

    with open("data/豆瓣电影top250.txt", 'a')as f:
        f.write(movie)


def crawl():
    """爬虫引擎"""
    # 爬虫入口
    url = "https://movie.douban.com/top250"
    # 发起请求获取响应
    html = html_download(url)
    #　得到电影和下一页数据
    movie,url_next = html_parser(html)
    # 保存数据
    dataoutput(movie)
    # 判断是否时最后一页
    if url_next == None:
        dataoutput(movie)
        print("下载完毕")
    # 发送下一页请求
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
