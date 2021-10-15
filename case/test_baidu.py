"""
unittest.skip(reason)：无条件的跳过修饰的测试，说明跳过测试的原因。

unittest.skipIf(condition,reason)：跳过修饰的测试，如果条件为真时。

unittest.skipUnless(condition,reason)：跳过修饰的测试，除非条件为真。

unittest.expectedFailure()：测试标记为失败。不管执行结果是否失败，统一标记为失败。
"""

from selenium import webdriver
import unittest
import time
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
import logging
from test_project.HTMLTestRunner import HTMLTestRunner

# logging.basicConfig(level=logging.DEBUG)


class Baidu(unittest.TestCase):
    """百度登录测试报告"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "http://www.baidu.com"

    def test_baidu(self):
        """界面登录按钮入口检查"""
        driver = self.driver
        driver.get(self.base_url + "/")
        ac = ActionChains(driver)
        # 开启debug模块，就可以捕捉到客户端向服务器发送的请求。
        # logging.basicConfig(level=logging.DEBUG)
        # CSS鼠标移动到 元素上
        ac.move_to_element(driver.find_element_by_css_selector('[name="tj_briicon"]')).perform()
        # 截取应用图片
        driver.get_screenshot_as_file(r'D:\web_pro\web_outo\Photo_screenshot\list.png')
        time.sleep(3)
        # 获取窗口大小
        print(driver.get_window_size())
        time.sleep(2)
        # 改变屏幕大小
        driver.set_window_size(width=875, height=950)
        # 获取浏览器地址
        print(driver.current_url)
        # 获得cookie信息
        cookies = driver.get_cookies()
        print("当前网站cookies为：", cookies)
        time.sleep(3)
        print("测试第一步")

        # 获取cookie中name的相关信息
        get_name = driver.get_cookie(name='H_PS_PSSID')
        print(get_name)
        time.sleep(3)
        print("测试第二步")

        # cookie新增信息
        driver.add_cookie({'name': 'v_Changchun', 'value': "Qangchen"})
        print(driver.get_cookies())
        time.sleep(3)
        print("测试第三步")

        # 遍历cookies中的name和value信息并打印
        for cookie in cookies:
            print("cookie相关信息已打印为:""%s -> %s" % (cookie['name'], cookie['value']))

        # Xpath定义登录按钮位置
        try:
            login = driver.find_element_by_xpath('//*[@id="s-top-loginbtn"]')
        except NoSuchElementException as e:
            print("找不到登录按钮，报错为：%s", e)
            driver.get_screenshot_as_file(r'D:\web_pro\web_outo\Photo_screenshot\error_one.png')
        # 鼠标悬停在登录按钮
        else:
            ActionChains(driver).move_to_element(login).perform()
            # 鼠标悬停在登录按钮
            time.sleep(3)
            print("点击登录按钮")
            # 点击登录按钮
            login.click()
            time.sleep(2)
            driver.get_screenshot_as_file(r'D:\web_pro\web_outo\Photo_screenshot\login.png')
            time.sleep(5)
        try:
            colsebtn = driver.find_element_by_class_name('close-btn')
        except NoSuchElementException as e:
            print("找不到关闭按钮，报错为：%s", e)
            driver.get_screenshot_as_file(r'D:\web_pro\web_outo\Photo_screenshot\error_two.png')
            time.sleep(2)
            print(r'报错截图已保存,截图路径为：D:D:\web_pro\web_outo\Photo_screenshot\error_two.png')
        else:
            # 点击关闭按钮
            colsebtn.click()
            print("关闭登录页面")
            driver.get_screenshot_as_file(r'D:\web_pro\web_outo\Photo_screenshot\success.png')
            time.sleep(2)
            print(r'扫码登录入口已关闭，保存log截图路径为：D:\web_pro\web_outo\Photo_screenshot\success.png')
            title = driver.title
            # print(title) 测试
            self.assertEqual(title, '百度一下，你就知道')

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    print(1111)
    testunit = unittest.TestSuite()
    testunit.addTest(Baidu("test_baidu"))
    # # 按照一定格式获取当前时间
    # file = time.strftime("%Y-%m-%d %H_%M_%S")
    # # 定义报告存放路径
    # re = r'D:\codetest\test_project\report\测试报告：'+file + ' result.html'
    # fp = open(re,'wb')
    # # 定义测试报告
    # runner = HTMLTestRunner(stream=fp,
    #                         title='百度搜索测试报告',
    #                         description='用例执行情况：',
    #                         verbosity=2
    #                         )
    # runner.run(testunit)  # 运行测试用例
    # fp.close() # 关闭报告文件
