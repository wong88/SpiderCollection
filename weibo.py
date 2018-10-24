import requests

class WeiBo:
    def __init__(self):
        self.url = 'https://weibo.com/?category=99991'

    def get_response(self):
        requests.get(self.url,)
    def run(self):
        # 发起请求,获取响应
        self.get_response()
        # 解析响应,获取内容

        # 保存

        #