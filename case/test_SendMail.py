from selenium import webdriver
import unittest
from web_outo.page.sendmail_page import SendMail
from web_outo.page.login_page import url, Login
import ddt
import time
import logging


@ddt.ddt()
class SendMailCase(unittest.TestCase):
    """QQ邮箱发送案例"""

    # 代表整个测试执行中只执行一次的前置条件
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()  # 最大窗口化
        cls.sendmail = SendMail(cls.driver)

    # 代表每条用例开始前都会执行
    def setUp(self):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def test_01(self):
        """正常邮件发送测试报告"""
        self.sendmail.login_QQ(autologin_button=True)
        self.sendmail.Send_Mail()
        self.assertTrue(self.sendmail.Send_mail_successfully())

    def test_02(self):
        """定时发送邮件测试报告"""
        self.sendmail.login_QQ(autologin_button=True)
        self.sendmail.Send_mail_regularly()
        self.assertTrue(self.sendmail.Timedsending_emailpage_verification())

    # 代表每条用例结束时执行一次
    def tearDown(self):
        self.driver.delete_all_cookies()  # 清除cookeis
        self.driver.refresh()  # 刷新页面

    #  代表所有用例结束后执行一次
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
