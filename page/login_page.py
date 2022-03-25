"""

编写人员：v_qangchen（丁钢平的爸爸）
使用所有的封装方法更加简洁的去封装登录方法，与login.py代码作为比较是否更加简单简洁的页面流程
注意！！！！ web自动化编写过程中一定要主要iframe和content的切换，当唯一元素无法定位时，首先排查是否涉及到iframe切换
定时发送弹窗相关的方法还未实现--待补充
使用所有的封装方法更加简洁的去封装登录方法，与login.py代码作为比较是否更加简单简洁的页面流程

"""
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from Common.base import Base

url = 'https://mail.qq.com/'


class Login(Base):
    #  QQ 邮箱登录窗口元素
    switcher_plogin = (By.XPATH, '//*[@id="switcher_plogin"]')
    input_user = (By.ID, "u")
    input_password = (By.ID, "p")
    login_button = (By.ID, "login_button")
    autologin_button = (By.CLASS_NAME, "low_login_wording")

    def Input_User(self, text):
        """再次封装账号输入"""
        self.sendKeys(self.input_user, text)

    def Input_Psw(self, text):
        """再次封装密码输入"""
        self.sendKeys(self.input_password, text)

    def Click_login_button(self):
        """登录按钮点击方法封装"""
        self.click(self.login_button)

    def Click_autologin_button(self):
        """点击自动登录"""
        self.click(self.autologin_button)

    def Click_switcher_button(self):
        """切换按钮点击方法封装"""
        self.click(self.switcher_plogin)

    def login_QQ(self, user: str = "1425000581", password: str = "Weishi@321", autologin_button=False):
        """
        测试电脑已登录QQ登录
        :param user: 登录账号
        :param password: 登录密码
        :param autologin_button: 元素状态判断
        """
        self.open_iframe('login_frame')
        self.Click_switcher_button()
        self.Input_User(user)
        self.Input_Psw(password)
        if autologin_button: self.Click_autologin_button()
        time.sleep(2)
        self.Click_login_button()
        time.sleep(2)
        self.switch_content()

    def Not_login_QQ(self, uesr: str = "1425000581", password: str = "Weishi@321", autologin_button=False):
        """
        测试电脑未登录QQ
        :param uesr: 登录账号
        :param password: 登录密码
        :param autologin_button: 元素状态返回
        :return:
        """
        self.open_iframe('login_frame')
        self.Input_User(uesr)
        self.Input_Psw(password)
        if autologin_button: self.Click_autologin_button()  # 以默认false做为开关去判断，autologin_button为实参判断是否打开开关
        time.sleep(2)
        self.Click_login_button()
        time.sleep(2)
        self.switch_content()

    # link方法获取到当前页面的元素text文本来判定是否成功
    def get_login_uesrname(self, a):
        """
        判断登录页面是否出现该元素，做校验用
        :param a: 页面已存在的link文案
        :return: 判断结果，文件存在输出文案，文案不存在输出False
        """
        try:
            t = self.driver.find_element_by_link_text(a)
            print(t)
            return t.text
        except NoSuchElementException:
            return False


if __name__ == '__main__':
    dirver = webdriver.Chrome()
    login_page = Login(dirver)
    dirver.get(url)
    time.sleep(2)
    login_page.Not_login_QQ(autologin_button=True)
    # login_page.Not_login_QQ(autologin_button=True)
    time.sleep(2)
    rulest = login_page.get_login_uesrname("退出")
    print(rulest)
    dirver.quit()
