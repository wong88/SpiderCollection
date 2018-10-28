import requests
from lxml import etree
import json
import time
import re
from pymysql import *


class Csdn:
    def __init__(self):
        # 构建起始url
        self.url = 'https://www.csdn.net/'
        self.headers = {
            'Cookie': 'dc_session_id=10_1534255781965.690329; uuid_tt_dd=1867337173782432197_20180814; TY_SESSION_ID=26d2661f-c8d1-453b-8cd1-d7f4092a7a5a; dc_tos=pdgfct; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1534255786; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1534255805; ADHOC_MEMBERSHIP_CLIENT_ID1.0=13b03884-df19-d6d6-638d-9a5330fde5f4',
            'Host': 'www.csdn.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        }

    def parse_url(self, url, headers):
        """获取入口网页信息"""
        # 获取推荐内容
        html = requests.get(url=url, headers=headers).content.decode('utf-8.36kr')
        return html

    def selector_html(self, html):
        """解析响应"""
        # 解析html
        selector = etree.HTML(html)
        # 通过规则匹配出url
        pp = '// *[ @ id = "feedlist_id"] / li[1] / div / div[1] / h2 / a//@href'
        # 将url添加进url列表
        url_list.extend(selector.xpath(pp))

    def download(self):
        """获取url，ajax页面请求"""
        # 设置记录文章篇数的变量
        j = 1
        while True:
            # 获取当前时间
            times = time.time()
            # 将获取到的时间进一步处理
            times = re.sub(r'\.', '', str(times))
            # 组装新的url
            url = 'http://blog.csdn.net/api/articles?type=more&category=home&shown_offset=%s' % times
            # 写请求头
            headers = {
                'Cookie': 'dc_session_id=10_1534255781965.690329; uuid_tt_dd=1867337173782432197_20180814; TY_SESSION_ID=9fc35a8a-24e0-4315-b1bc-9b04f6334fbe; dc_tos=pdho5u; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1534255786,1534312488; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1534313875; ADHOC_MEMBERSHIP_CLIENT_ID1.0=c6e82287-0101-9aa8-347a-0a41269a9182',
                'Host': 'blog.csdn.net',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                'Upgrade-Insecure-Requests': '1'
            }
            # 获取ajax
            ajks_url = requests.get(url=url, headers=headers).content.decode('utf-8.36kr')
            # 将获取到的ajax转化为python里的格式
            html_url = json.loads(ajks_url)
            # 切换到articles目录
            html_url = html_url['articles']
            # 获取长度
            page = len(html_url)
            # # 遍历获取的url列表
            for i in range(0, page):
                # 获取我们需要的url
                bk_url = html_url[i]['url']
                # 去重
                if bk_url not in url_list:
                    # 将去重的url添加进新的url列表
                    url_list.append(bk_url)
                    # 获取文章标题,分类,作者,阅读数,时间,url地址信息
                    bk_title = html_url[i]['title']
                    bk_category = html_url[i]['category']
                    bk_nickname = html_url[i]['nickname']
                    bk_views = html_url[i]['views']
                    bk_createdat = html_url[i]['created_at']
                    # 数据库去重处理
                    if bk_url not in urlqc_list:
                        # 把获取的数据存入数据库
                        reserve(bk_url, bk_title, bk_category, bk_nickname, bk_views, bk_createdat)
                        # 输出获取信息
                        print('一获取%s篇文章' % j)
                        # 输出信息后变量增加
                        j += 1
                        # 将去重后的url添加进去重列表
                        urlqc_list.append(i)
                    return bk_title, bk_category, bk_nickname, bk_views, bk_createdat

    def reserve(self, bk_url, bk_title, bk_category, bk_nickname, bk_views, bk_createdat):
        """url处理"""
        # 连接数据库
        conn = connect(host='', port=3306, user='', password='', database='', charset='utf8')
        # 添加游标对象
        cs = conn.cursor()
        # 添加数据
        cs.execute('insert into blogurl values(0,%s,%s,%s,%s,%s,%s);',
                   (bk_title, bk_category, bk_nickname, bk_views, bk_createdat, bk_url))
        # 事务确认
        conn.commit()
        # 将获取的url添加进去重列表
        time.sleep(0.01)
        # 关闭游标对象
        cs.close()
        # 关闭数据库对象
        conn.close()

    def run(self):
        """控制引擎"""
        html = self.parse_url(self.url, self.headers)
        self.selector_html(html)
        # 启动获取ajax的函数
        bk_title, bk_category, bk_nickname, bk_views, bk_createdat = self.download()
        self.reserve(bk_title, bk_category, bk_nickname, bk_views, bk_createdat)


if __name__ == '__main__':
    url_list = list()
    urlqc_list = list()
    csdn = Csdn()
    csdn.run()
