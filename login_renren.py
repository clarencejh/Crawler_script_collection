# 模拟登录人人网

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

# 设置账号和密码
data = {
        'email': 'username',
        'password': 'password'
    }

login_url = 'http://www.renren.com/PLogin.do'
dapeng_url = 'http://www.renren.com/880151247/profile'

def login():
    session = requests.Session()

    # 这里返回一个 response ,同时设置cookies

    page = session.post(login_url, headers=headers, data=data)
    print(session.cookies)

    # 用包含cookies的对象 请求一个网站测试
    resp = session.get(dapeng_url)
    with open('demo6_requests.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)

# 测试成功
if __name__ == "__main__":
    login()
