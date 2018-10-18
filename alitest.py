import requests,random

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.9 Safari/537.36'
        }



            # print(pageIndex)

t = '%0.16f' % random.random()

data = {'pageSize': "10", 't': str(t), 'pageIndex': 3}
            # print(data)
    #         data= {
    #     "pageSize": "10",
    #     "t": "0.4459761467958639",
    #     "pageIndex": 3
    # }

# res = requests.post(
#     "https://job.alibaba.com/zhaopin/socialPositionList/doList.json",
#     headers=headers,
#     data={
#         "pageSize": "10",
#         "t": "0.4459761467958639",
#         "pageIndex": 3
#     })

res = requests.post(
    "https://job.alibaba.com/zhaopin/socialPositionList/doList.json",
    headers=headers,
    data=data)
# {'pageIndex': 2, 'pageSize': '20', 't': '0.68131939'}

print(res.text)