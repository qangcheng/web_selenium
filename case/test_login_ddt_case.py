"""
用例编写人员：丁钢平的爸爸（v_QiangChen）
用例设计保证用例独立性，且用例最后都是为校验处理
用例执行完成后记得做数据清理
此测试用例根据之前page优化过的登录页面封装库来调用，相比test_login更加参数化和可维护性更高，日志相关输出更高清晰明了，方便定位问题
ddt为独立框架数据分离，运行时记得不要运行单个用例，需要运行整个框架在if_main处运行
ddt好处在于对于同样用例只是数据不一致的用例执行时，更加优化代码的耦合性，可以单个数据形成测试结果，使用for循环的话，这样测试只是一个结果
"""

from selenium import webdriver
import unittest
from web_outo.page.login_page import Login, url
import ddt
import time


# 测试数据源
# testdates = [
#     {"user": "1425000581", "psw": "Weishi@321", "Except": "退出"},
#     {"user": "1425000581", "psw": "weishi999", "Except": ""},
#     {"user": "1425000581", "psw": "", "Except": ""}
# ]


@ddt.ddt()
class LoginCase(unittest.TestCase):
    """QQ邮箱登录案例"""

    # 代表整个测试执行中只执行一次的前置条件
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()  # 最大窗口化
        cls.Login_page = Login(cls.driver)

    # 代表每条用例开始前都会执行
    def setUp(self):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    # 登录用例测试流程
    def login_case(self, user, psw, Except):
        # 第一种自己写流程
        self.Login_page.open_iframe('login_frame')
        self.Login_page.Click_switcher_button()
        self.Login_page.Input_User(user)
        self.Login_page.Input_Psw(psw)
        if self.Login_page.autologin_button: self.Login_page.Click_autologin_button()
        time.sleep(2)
        self.Login_page.Click_login_button()
        self.Login_page.switch_content()
        result = self.Login_page.get_login_uesrname(Except)
        print("测试结果为：%s" % result)
        self.assertTrue(result == Except)  # 所有测试用例最后一定是做页面校验，判断是否成功
        # 第二种,自己调用页面已写好的流程
        # self.Login_page.login_QQ()

    @ddt.data({"user": "1425000581", "psw": "Weishi@321", "Except": "退出"},
              {"user": "1425000581", "psw": "weishi999", "Except": ""},
              {"user": "1425000581", "psw": "", "Except": ""})
    # 正确账号密码
    def test_01(self, data):
        """QQ邮箱登录成功测试报告"""
        print("--------------开始测试：test_01--------------")
        # data1 = testdates[0]
        print("测试数据是：%s" % data)
        self.login_case(data["user"], data["psw"], data["Except"])
        print("--------------结束测试：End!!-----------------")

    # # 错误账号密码
    # def test_02(self):
    #     """QQ邮箱登录失败测试报告 """
    #     print("--------------开始测试：test_02--------------")
    #     data1 = testdates[1]
    #     print("测试数据是：%s" % data1)
    #     self.login_case(data1["user"], data1["psw"], data1["Except"])
    #     print("--------------结束测试：end!!-----------------")
    #
    # # 空账号密码
    # def test_03(self):
    #     """QQ邮箱登录失败测试报告 """
    #     print("--------------开始测试：test_03--------------")
    #     data1 = testdates[2]
    #     print("测试数据是：%s" % data1)
    #     self.login_case(data1["user"], data1["psw"], data1["Except"])
    #     print("--------------结束测试：end!!-----------------")

    # 代表每条用例结束时执行一次
    def tearDown(self):
        self.Login_page.is_alert_exist()
        self.driver.delete_all_cookies()  # 清除cookeis
        self.driver.refresh()  # 刷新页面

    #  代表所有用例结束后执行一次
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # 编辑器问题


if __name__ == '__main__':
    unittest.main()
