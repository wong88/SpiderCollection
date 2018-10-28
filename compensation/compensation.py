import urllib.request
from lxml import etree
import re


def main(url, headers):
    # 爬虫调度
    resp = html_down(url, headers)
    analysis(resp)
    for urls in url_list:
        resp_body = html_down(url=urls, headers=headers)
        content_download(resp_body, urls)


def html_down(url, headers):
    # 页面下载
    request = urllib.request.Request(url=url, headers=headers)
    resp = urllib.request.urlopen(request).read().decode('utf-8', 'replace')
    return resp


def analysis(resp):
    # url获取
    # content = re.findall(r'<div align="center">.*<div align="center">',resp)
    selector = etree.HTML(resp)
    subjects_salary_url_list = selector.xpath(
        '//table [@class="t_table"]/tr/td/div/a/@href | '
        '//table [@class="t_table"]/tr/td/div/div/div/a/@href |'
        '//table [@class="t_table"]/tr/td/div/div/div/div/a/@href ')
    # print(subjects_salary_url_list)
    for i in subjects_salary_url_list:
        url_list.append(i)


def content_download(resp, urls):
    # 内容获取
    if re.match(r'.*411899', urls):
        xpath_rule = '//table [@class="t_table"]/tr[1]/td/div/strong/font/text() |' \
                     '//table [@class="t_table"]/tr/td/div/font/font/strong/text() |' \
                     '//table [@class="t_table"]/tr/td [@ width ="85"]/div/text()'
        javaee_salary_list = selectorbase(xpath_rule, resp)
        sum = 0
        for i in javaee_salary_list:
            sum += float(i)
        avg = sum / len(javaee_salary_list)
        print(avg)
        print(javaee_salary_list)
    elif re.match(r'.*411903', urls):
        xpath_rule = '//table [@class="t_table"]/tr[1]/td/div/font/font/strong/text() ' \
                     '//table [@class="t_table"]/tr/td [2]/div/text() |' \
                     '//table [@class="t_table"]/tr/td [2]/div/div/text()'
        php_h5_salary_list = selectorbase(xpath_rule, resp)
        sum = 0
        for i in php_h5_salary_list:
            sum += float(i)
        avg = sum / len(php_h5_salary_list)
        print(len(php_h5_salary_list))
        print(avg)
        print(php_h5_salary_list)
    elif re.match(r'.*411905', urls):
        xpath_rule = '//table [@class="t_table"]/tr[1]/td/div/strong/font/text() |' \
                     '//table [@class="t_table"]/tr/td/div/strong/font/font/text()' \
                     '//table [@class="t_table"]/tr/td[2]/div/div/text()'
        c_cadd2_salary_list = selectorbase(resp=resp, xpath_rule=xpath_rule)

        sum = 0
        for i in c_cadd2_salary_list:
            sum += float(i)
        avg = sum / len(c_cadd2_salary_list)
        print(len(c_cadd2_salary_list))
        print(avg)
        print(c_cadd2_salary_list)
    elif re.match(r'.*411907', urls):
        xpath_rule = '//table [@class="t_table"]/tr[1]/td/div/font/strong/text() |' \
                     '//table [@class="t_table"]/tr/td/div/font/font/strong/text() ' \
                     '//table [@class="t_table"]/tr/td[2]/div/div/text() '
        ui_ue_salary_list = selectorbase(xpath_rule, resp)
        sum = 0
        for i in ui_ue_salary_list:
            sum += float(i)
        avg = sum / len(ui_ue_salary_list)
        print(len(ui_ue_salary_list))
        print(avg)
        print(ui_ue_salary_list)
    elif re.match(r'.*411908', urls):
        xpath_rule = '//table [@class="t_table"]/tr[1]/td/div/strong/font/text() |' \
                     '//table [@class="t_table"]/tr/td/div/strong/font/font/text()' \
                     '//table [@class="t_table"]/tr/td[2]/div/div/text()'
        html_salary_list = selectorbase(xpath_rule, resp)
        sum = 0
        for i in html_salary_list:
            sum += float(i)
        avg = sum / len(html_salary_list)
        print(len(html_salary_list))
        print(avg)
        print(html_salary_list)
    elif re.match(r'.*411923', urls):
        xpath_rule = '//table [@class="t_table"]/tr[1]/td/div/strong/font/text()|' \
                     '//table [@class="t_table"]/tr/td/div/strong/font/font/text()' \
                     '//table [@class="t_table"]/tr/td[2]/div/div/text()'
        python_salary_list = selectorbase(xpath_rule, resp)
        sum = 0
        for i in python_salary_list:
            sum += float(i)
        avg = sum / (len(python_salary_list) - 1)
        print(len(python_salary_list))
        print(avg)
        print(python_salary_list)
        print(python_salary_list)


def selectorbase(xpath_rule, resp):
    selector = etree.HTML(resp)
    return selector.xpath(xpath_rule)


if __name__ == '__main__':
    url = 'http://bbs.itheima.com/forum.php?mod=viewthread&tid=130723?szt1'
    headers = {
        'Cookie': 'UM_distinctid=1642b2ae1b24bb-09eed5e35986d9-514b2f1f-144000-1642b2ae1b33cb; bad_idd48d5cf0-2e47-11e8-9db3-3313a60c92e9=508029c1-76a8-11e8-b3e6-73ea0cfe010b; mcb9_2132_saltkey=S8HAAe70; mcb9_2132_lastvisit=1535783921; _uab_collina=153578782092825687860764; mcb9_2132_client_created=1536301135; mcb9_2132_client_token=D5A80D51163184864CD40C55C0CE002F; mcb9_2132_auth=d739KZffLkg4uwjsT%2BoYd6U2vS5umpjcXvpkQajJCw1LGIn3hLx%2FjfGtFYTwARovbzbeoDZ%2Fx3rZjaoKveGKvH2N%2Fls; mcb9_2132_connect_login=1; mcb9_2132_connect_is_bind=1; mcb9_2132_connect_uin=D5A80D51163184864CD40C55C0CE002F; mcb9_2132_smile=5D1; mcb9_2132_atarget=1; nice_idd48d5cf0-2e47-11e8-9db3-3313a60c92e9=641f0c01-b7b5-11e8-93fa-c5b2674f8255; mcb9_2132_security_cookiereport=26d1gFitEOA1XiTt3AxpXFEhnVkhSNrsSzhdznnbEUG0NLIwdQkA; mcb9_2132_pc_size_c=0; mcb9_2132_gfcity=430; mcb9_2132_ulastactivity=ee9d4tWoMt8GZ1u%2FmMFkMeoA9WiYEIg4DrUGabXKZfvzeisacVIP; Hm_lvt_7ea6c0c8412eb91d6e44a2459dc4ae81=1535787824,1536301118,1536885044; CNZZDATA3092227=cnzz_eid%3D874273581-1535786544-http%253A%252F%252Fwww.itheima.com%252F%26ntime%3D1536881614; openChatd48d5cf0-2e47-11e8-9db3-3313a60c92e9=true; mcb9_2132_visitedfid=236D472D454D426D237; mcb9_2132_st_t=459993%7C1536885314%7Cf89e038a39df4f3b429df5c1bdafc8f6; mcb9_2132_forum_lastvisit=D_472_1536313432D_236_1536885314; mcb9_2132_st_p=459993%7C1536885602%7C356f16357111f7e89a635cbd5394f54f; mcb9_2132_viewid=tid_130723; mcb9_2132_lastcheckfeed=459993%7C1536885603; Hm_lpvt_7ea6c0c8412eb91d6e44a2459dc4ae81=1536885604; security_session_verify=a5a3f311957197ea0c8e680d4e8e3242; mcb9_2132_sid=Pg6u4g; mcb9_2132_lip=183.95.50.225%2C1536889120; mcb9_2132_lastact=1536889125%09forum.php%09misc',
        'Host': 'bbs.itheima.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3514.0 Safari/537.36',
    }
    url_list = list()
    main(url, headers)





    # '//table [@class="t_table"]/tr/td/div/text()'
    # '//table [@class="t_table"]/tr/td/div/div/text()')
    # '//table [@class="t_table"]/tr/td [@ width ="121"]/div/text()')
    # '//table [@class="t_table"]/tr/td [@ width="97"]/div/div/text()'
    # '//table [@class="t_table"]/tr/td/div/font/font/strong/text() |'
    # '//table [@class="t_table"]/tr/td/div/strong/text()'
    # '//table [@class="t_table"]/tr/td/div/a/@href '
    # '//table [@class="t_table"]/tr/td/div/strong/font/text()'