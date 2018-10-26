import requests
import re
from pymysql import *

nndl = dict()


def main(url, headers):
    q = 1
    # 建立数据库连接
    conn = connect(host='', port=3306, database='', user='', password='', charset='utf8')
    # 获取游标对象
    db = conn.cursor()
    # 　发送请求
    html = requests.get(url=url, headers=headers).content.decode('utf-8')
    #  获取ip
    temp = re.findall(r'<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>', html)
    # 获取port
    temp2 = re.findall(r' <td class="country">高匿</td>\s+<td>(HTTP(S)?)</td>', html)
    # sql语句
    sql = 'insert into account values(0,%s,%s,%s)'
    print(temp2)
    # 遍历
    for i, j in zip(temp, temp2):
        # 　向数据库中插入数据
        db.execute(sql, (i[0], i[1], j[0]))
        # print(j)
        # 提交数据
        conn.commit()
        print('写入%d条数据成功' % q)
        q += 1
    # 关闭数据库对象
    db.close()
    # 关闭连接
    conn.close()


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
