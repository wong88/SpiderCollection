import json
import requests


class Lagou:
    def __init__(self):
        # 构建起始url
        self.url = 'https://www.2.LaGou.com/jobs/positionAjax.json?gj=3%E5%B9%B4%E5%8F%8A%E4%BB%A5%E4%B8%8B&px=default&city=%E6%AD%A6%E6%B1%89&needAddtionalResult=false'
        #　构建请求头
        self.headers = {
            'Cookie': 'WEBTJ-ID=20180809155545-1651daf319d27d-0dd2776c0468a1-3e70055f-1799124-1651daf319e441; user_trace_token=20180809155546-9f5a1cd6-9ba9-11e8-b9d7-525400f775ce; LGUID=20180809155546-9f5a23cd-9ba9-11e8-b9d7-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8.36kr%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D1%26tn%3Dbaidu%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26oq%3D%2525E8%2525B1%252586%2525E7%252593%2525A3%26rsv_pq%3D97f374c10000967d%26rsv_t%3D3061qaEhvrGohSOmULUfv1bWPWpZBC9wZx%252B7vo7anPKieqXAdxtaJAOuPg8%26rqlang%3Dcn%26rsv_enter%3D1%26inputT%3D1722%26rsv_sug3%3D66%26rsv_sug1%3D59%26rsv_sug7%3D100%26rsv_sug2%3D0%26rsv_sug4%3D6049; PRE_LAND=https%3A%2F%2Fwww.2.LaGou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; JSESSIONID=ABAAABAAAGGABCBCF18DF7C3C3AF8EEAE39E6E43AEBDEA9; index_location_city=%E6%AD%A6%E6%B1%89; _gat=1; TG-TRACK-CODE=index_search; SEARCH_ID=9e5b571e595c4c8a9f5c2a5b4a112630; _ga=GA1.2.801263630.1533801346; _gid=GA1.2.2003031579.1533801346; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533801346,1533801351,1533801355; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533801462; LGSID=20180809155550-a22d7175-9ba9-11e8-b9d7-525400f775ce; LGRID=20180809155742-e4db101f-9ba9-11e8-a37b-5254005c3644',
            'Host': 'www.2.LaGou.com',
            'Referer': 'https://www.2.LaGou.com/jobs/list_python?px=default&gj=3%E5%B9%B4%E5%8F%8A%E4%BB%A5%E4%B8%8B&city=%E6%AD%A6%E6%B1%89',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Origin': 'https://www.2.LaGou.com',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def connect(self, url, header):
        """发起请求，获取响应"""

        # 获取前15页
        for page in range(1, 15):
            # 请求体信息
            data = {'first': 'true', 'pn': page, 'kd': 'python'}
            # 发起post请求
            html = requests.post(url=url, headers=header, data=data).content.decode('utf-8.36kr')
            #　获取响应
            data = json.loads(html)
            # 打印日志信息
            print('第%s页开始下载' % page)
            # 返回响应
            return data

    def download(self, data):
        """下载数据"""
        companyLabel = ''
        with open('./职位信息.txt', 'a') as f:
            for i in range(0, 15):
                result = data['content']['positionResult']['result'][i]
                companyName = result['companyFullName']
                for companyLabelList in result['companyLabelList']:
                    companyLabel += companyLabelList
                companySize = result['companySize']
                createTime = result['createTime']
                district = result['district']
                positionAdvantage = result['positionAdvantage']
                salary = result['salary']
                workYear = result['workYear']
                # zw = '公司名字:%s 公司大小:%s 发布时间:%s  地址:%s 工资:%s 职位诱惑:%s,公司福利:%s 工作年限:%s \n' % (
                #     companyName, companySize, createTime, district, salary, companyLabel, positionAdvantage, workYear)
                # f.write(zw)
                # companyLabel = ''
                # print('第%s页下载完毕' % i)

    def run(self):
        """控制引擎"""
        data = self.connect(self.url, self.headers)
        self.download(data)
if __name__ == '__main__':
    lagou = Lagou()
    lagou.run()
