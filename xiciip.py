import requests
import re
from pymysql import *

nndl = dict()


def main(url, headers):
    q = 1
    conn = connect(host='localhost', port=3306, database='ipport', user='root', password='mysql', charset='utf8')
    db = conn.cursor()
    html = requests.get(url=url, headers=headers).content.decode('utf-8')
    temp = re.findall(r'<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>', html)
    temp2 = re.findall(r' <td class="country">高匿</td>\s+<td>(HTTP(S)?)</td>',html)
    sql = 'insert into account values(0,%s,%s,%s)'
    print(temp2)
    for i,j in zip(temp,temp2):
        db.execute(sql, (i[0], i[1],j[0]))
        # print(j)
        conn.commit()
        print('写入%d条数据成功' % q)
        q += 1
    db.close()
    conn.close()
    # print(temp)
    # for i in temp:
    # sql
    # db.execute()


if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTU0MGQxYjhhY2QwMWU5YWYwZGU0YWU2MDJkZTcwZjkxBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXEzVzZOMlhxekwzMmQ5ZzVWNGwzQTZINkhyVDgxRTJFaVVJUmdVMzlsdE09BjsARg%3D%3D--a704b9d19c8faabcbbd7742ed63fefe4b134a5b4; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1534427576; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1534428369',
        'Host': 'www.xicidaili.com',
        'If-None-Match': 'W/"0eab563b12364a2977dddd79a38d86f9"',
        # 'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    main(url, headers)
