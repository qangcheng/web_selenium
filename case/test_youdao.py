from selenium import webdriver
import unittest
import time
from test_project.HTMLTestRunner import HTMLTestRunner


class MyTest(unittest.TestCase):
    """有道web测试报告"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "http://www.youdao.com"

    def test_YouDao(self):
        """登录测试"""
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("translateContent").clear()
        driver.find_element_by_id("translateContent").send_keys("webdriver")
        driver.find_element_by_xpath('//*[@id="form"]/button').click()
        time.sleep(2)
        title = driver.title
        self.assertEqual(title, "【webdriver】什么意思_英语webdriver的翻译_音标_读音_用法_例句_在线翻译_有道词典")
        # 打印当前页面代码
        print(driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
