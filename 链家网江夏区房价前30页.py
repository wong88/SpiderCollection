import re
import requests
from bs4 import BeautifulSoup


def download(heands, url):
    '''下载数据'''
    i = 0
    while i <= 30:
        result = requests.get(url=url, headers=heands)
        temp = result.text
        bf = BeautifulSoup(temp, 'lxml')
        temp = bf.findAll('ul', class_="resblock-list-wrapper")
        # name = bf.findAll('a', class_='name')
        with open("./数据/武汉江夏区房价(前30页).txt", "a", encoding='utf-8') as f:
            f.write(str(temp))
        i += 1


def Resolve():
    '''解析数据'''
    with open('./数据/武汉江夏区房价(前30页).txt', 'r', encoding='utf-8') as f:
        content = f.read()

    bf = BeautifulSoup(content, 'lxml')
    temp = bf.find_all('a')
    contents = ''
    for i in temp:
        contents += i.get_text() + ' '
    result = re.sub(r'(效果图|\n|\d\.\d折)', '', contents)
    result = re.sub(r'(\s\s)+', '\n', result)
    temp = bf.find_all('span')
    temps = ''
    for i in temp:
        temps += i.text + ' '

    def jx(bq, temp, name_list, ):
        name_list = list()
        temp = bf.findAll(bq, class_=temp)
        for i in temp:
            name_list.append(i.text)
        return name_list

    name = jx('a', 'name', 'name_list')
    resblock_type = jx('span', 'resblock-type', 'type_list')
    sale_status = jx('span', 'sale-status', 'status_list')
    price = jx('span', 'number', 'number_list')
    j = 0
    with open('./数据/江夏区房屋信息.txt', 'a', encoding='utf-8') as f:
        while j < len(price):
            content += '楼盘：%s  房屋属性：%s   开售时间：%s    价格：%s' % (name[j], resblock_type[j], sale_status[j], price[j])
            j += 1
        content = re.sub(r'(^<(.*)$>|\n)', '', content)
        print(content)
        f.write(content)


if __name__ == '__main__':
    heands = {
        'Cookie': 'lianjia_ssid=a1b8676b-c1f1-4ad8-a61c-3531ca925247; lianjia_uuid=0a23a7fd-bb45-4d3d-bd29-a7c8b0dc9f6c; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1533116384; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1533116384; _smt_uid=5b617fe0.49e6ecd4; UM_distinctid=164f4db8366221-0a02f2cad90187-737356c-144000-164f4db83671c0; _jzqa=1.4102213568481723400.1533116384.1533116384.1533116384.1; _jzqc=1; _jzqckmp=1; _jzqb=1.1.10.1533116384.1; _ga=GA1.2.755981037.1533116386; _gid=GA1.2.1672307155.1533116386; _jzqa=1.4102213568481723400.1533116384.1533116384.1533116384.1; _jzqc=1; select_city=420100; CNZZDATA1256296306=793497127-1533111794-https%253A%252F%252Fbj.fang.lianjia.com%252F%7C1533111794; CNZZDATA1254525948=786597468-1533111385-https%253A%252F%252Fbj.fang.lianjia.com%252F%7C1533111385; CNZZDATA1255633284=481621688-1533113030-https%253A%252F%252Fbj.fang.lianjia.com%252F%7C1533113030; CNZZDATA1255604082=467122936-1533115496-https%253A%252F%252Fbj.fang.lianjia.com%252F%7C1533115496; _qzjc=1; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _qzja=1.1789345286.1533116414854.1533116414854.1533116414854.1533116435203.1533116492631.0.0.0.4.1; _qzjb=1.1533116414854.4.0.0.0; _qzjto=4.1.0; _jzqb=1.2.10.1533116384.1; lj_newh_session=eyJpdiI6Iml3K3JvRll5dzcwS1dlMDFuV1FoTVE9PSIsInZhbHVlIjoid1BjM1lMSXVXVVlDZUJOTGdiMCtqMWpqWENHMGpldlRJSTQxNFo3MlNkSU5vSFdtd3Ruc0sydHNRdnlXM1wvMFJ1c21ySmkwTHQ3RTBGRlwvaElKeGRMdz09IiwibWFjIjoiY2E1ZDA3NDgyNzY4NzRmMTY2YTBmNDc2MjczOGVjZjM5NmZmYWIyNjBlYWU5YzZlNDg1N2JjNWVmN2VmZjcwNCJ9',
        'Host': 'wh.fang.lianjia.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    url = 'https://wh.fang.lianjia.com/loupan/jiangxia/pg' + str(i) + '/#jiangxia'
    download(heands, url)
