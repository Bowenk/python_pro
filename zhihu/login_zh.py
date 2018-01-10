
# !coding=utf-8
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pickle


class BaiduSpider(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.get(url='http://www.zhihu.com')
        self.set_cookie()
        self.is_login()

    def is_login(self):
        '''判断当前是否登陆'''
        self.driver.refresh()
        html = self.driver.page_source

        # if not html:
        #     print("html is null")
        # else:
        #   # soup = BeautifulSoup(html, "lxml")
        #     target = self.driver.find_elements_by_tag_name("_blank")
        #     for t in target:
        #         print(t.text)

        if html.find(self.username) == -1:  # 利用用户名判断是否登陆
            # 没登录 ,则手动登录
            self.login()
        else:
            # 已经登录 尝试访问搜索记录，可以正常访问
            self.driver.get(url='https://www.zhihu.com/')
            time.sleep(30)  # 延时看效果

    def login(self):
        '''登陆'''
        time.sleep(60)  # 等待手动登录
        self.driver.refresh()
        self.save_cookie()

    def save_cookie(self):
        '''保存cookie'''
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def set_cookie(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    "domain": cookie.get('domain'),  # 火狐浏览器不用填写，谷歌要需要
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expiry": cookie.get('expiry'),
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': True,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    BaiduSpider('bowenk', '***')  #知乎账号 密码