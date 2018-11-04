import requests
from retrying import retry



@retry(stop_max_attempt_number=3)
def _parse_url(url, headers=None):
    print('*' * 10)
    session = requests.session()
    response = session.get(url, headers=headers, timeout=3)
    assert response.status_code == 200
    return response.content.decode()


def parse_url(url, headers=None):
    try:
        response_str = _parse_url(url, headers)
    except Exception as e:
        print(e)
        response_str = None
    return response_str


if __name__ == '__main__':
    url = ''
    parse_url(url)
