import requests
import re
import json


def main(url):
    response = requests.get(url).content.decode()
    title = re.findall(r'"title":"(.*?)"', response)
    content = re.findall(r'"description":"(.*?)"', response)
    url = re.findall(r'"news_url":"(.*?)"', response)
    '''
    b_id: 138742
    per_page: 20
    _: 1538228332451
     '''
    ajax_url = 'https://36kr.com/api/newsflash?b_id=138742&per_page=20&_=1538228332451'
    headers = {'Referer': 'https://36kr.com/newsflashes',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/70.0.3538.9 Safari/537.36',
               'X-Tingyun-Id': 'Dio1ZtdC5G4;r=228332452'}
    data_str = requests.get(url=ajax_url, headers=headers).content.decode()
    data_dict = json.loads(data_str)
    items = data_dict["data"]["items"]
    new_title_list = []
    new_content_list = []
    new_news_url_list = []
    for i in items:
        new_title = i["title"]
        new_title_list.append(new_title)
        new_content = i["description"]
        new_content_list.append(new_content)
        new_news_url = i["news_url"]
        new_news_url_list.append(new_news_url)
    print(len(items))
    print(new_title_list)
    print(new_content_list)
    print(new_news_url_list)


if __name__ == '__main__':
    url = 'https://36kr.com/newsflashes'
    main(url)

