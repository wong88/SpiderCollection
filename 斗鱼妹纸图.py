import requests
from lxml import etree


def down(url, headers):
    # html爬取
    html = requests.get(url=url, headers=headers).content.decode('utf-8')
    resolve(html)


def resolve(html):
    # 图片解析
    # // *[ @ id = "live-list-contentbox"] / li[1] / a / span / img
    selector = etree.HTML(html)
    # 电影名称
    photo = selector.xpath('//*[@id="live-list-contentbox"]/li/a/span/img/@src')
    length = len(photo)
    for i in range(0,length):
        download(photo)

def download(photo):
    '''图片下载'''
    with open('./斗鱼小姐姐.html','wb') as f:
        f.write(photo)

if __name__ == '__main__':
    url = 'https://www.douyu.com/g_ecy'
    headers = {
        'cookie': 'dy_did=151e13d0012e7cdbdf642d3400071501; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1536754317; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1536754672; smidV2=2018091220170334e2edf57f2ef64d273a96a97eaa183f00e269a170c175690; acf_did=151e13d0012e7cdbdf642d3400071501',
        'referer': 'https://www.douyu.com/g_kepu',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    }
    down(url, headers)
