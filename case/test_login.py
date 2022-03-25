"""
用例编写人员：丁钢平的爸爸（v_QiangChen）
用例设计保证用例独立性，且用例最后都是为校验处理
用例执行完成后记得做数据清理
"""

from selenium import webdriver
import unittest
from page.login import Login_Ulis
import logging

url = 'https://mail.qq.com/'


class Login(unittest.TestCase):
    """QQ邮箱登录案例"""
    # 代表整个测试执行中只执行一次的前置条件
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()  # 最大窗口化
        cls.Login = Login_Ulis(cls.driver)

    # 代表每条用例开始前都会执行
    def setUp(self):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    # 正确账号密码
    def test_01(self):
        """QQ邮箱登录成功测试报告"""
        self.Login.login("1425000581", "weishi")
        t = self.Login.get_login_uesrname("退出")
        self.assertTrue(t == "退出")

    # 错误账号密码
    def test_02(self):
        """QQ邮箱登录失败测试报告 """
        self.Login.login("1425000581", "weishi9999")
        t = self.Login.get_login_uesrname("退出")
        self.assertTrue(t == "")

    # 代表每条用例结束时执行一次
    def tearDown(self):
        self.Login.is_alert_exist()
        self.driver.delete_all_cookies()  # 清除cookeis
        self.driver.refresh()  # 刷新页面

    #  代表所有用例结束后执行一次
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # 编辑器问题


if __name__ == '__main__':
    unittest.main()
