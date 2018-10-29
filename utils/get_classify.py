import re

from lxml import etree

from utils.parse_url import parse_url


def get_classify(classify_url, headers):
    classify_list = []
    original_list = []
    response = parse_url(classify_url, headers)
    # 解析html
    selector = etree.HTML(response)
    '''/html/body/div[2]/div[1]/section[5]/div/ul/li[1]/a'''
    pp = '// ul [ @class = "type-list"] / li / a//@href'
    temp = selector.xpath(pp)
    for i in temp:
        classify = re.match(r'/tv/(\w+)', i).group(1)
        original_list.append(classify)
        if classify == 'british':
            classify = 'english'
        elif classify == 'korean':
            classify = 'korean_drama'
        elif classify == 'chinese':
            classify = 'domestic'
        elif classify == 'tvshow':
            classify = 'variety'
        classify_list.append(classify)

    return classify_list,original_list


if __name__ == '__main__':
    classify_url = 'https://m.douban.com/tv/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Mobile Safari/537.36',
        'Referer': 'https://m.douban.com/tv/american'
    }
    get_classify(classify_url, headers)
