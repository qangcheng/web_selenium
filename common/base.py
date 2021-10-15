from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标事件库
from selenium.webdriver.support.ui import Select  # 针对选项框的方法
import logging.config
import csv

# 读取log.conf中的配置表
CON_LOG = '../config/log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()


class Base(object):
    """基于selenium中的expected_conditions库做二次封装"""

    def __init__(self, driver=webdriver.Chrome()):
        self.new = time.strftime("%Y-%m-%d %H_%M_%S")
        self.driver = driver
        self.timeout = 10
        self.t = 0.5

    # 新的定位方法,与findElement方法返回一致
    def findElementNew(self, locator):
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元组类型：loc=("id","value1")')
        else:
            print("正在点各位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            ele = WebDriverWait(self.driver, self.timeout, self.t).until(lambda x: x.find_element(*locator))
            return ele

    # 单个元素等待方法封装，调用这个方法可以返回定位元素，比sleep和隐示等待更加稳定
    def findElement(self, locator):
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元组类型：loc=("id","value1")')
        else:
            print("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            ele = WebDriverWait(self.driver, self.timeout, self.t).until(lambda x: x.find_element(*locator))
            return ele

    # 一组元素等待方法封装，调用这个方法可以返回定位元素，比sleep和隐示等待更加稳定
    def findElements(self, locator):
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元组类型：loc=("id","value1")')
        else:
            print("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            ele = WebDriverWait(self.driver, self.timeout, self.t).until(lambda x: x.find_elements(*locator))
            return ele

    # 单个判断元素是否选中，使用多个弹窗选择判断
    def isSelected(self, locator):
        """判断元素是否被选中，返回bool值"""
        ele = self.findElement(locator)
        r = ele.is_selected()
        return r

    # 单个元素判断是否存在
    def isElementExist(self, locator):
        try:
            self.findElement(locator)
            return True
        except:
            return False

    # 多个元素判断是否存在
    def isElementsExist(self, locator):
        eles = self.findElements(locator)
        n = len(eles)
        if n == 0:
            return False
        elif n == 1:
            return True
        else:
            print("定位到多个元素：%s" % n)
            return True

    # 封装input方法
    def sendKeys(self, locator, text):
        ele = self.findElement(locator)
        return ele.send_keys(text)

    # 封装点击方法
    def click(self, locator):
        ele = self.findElement(locator)
        return ele.click()

    # 切换到html登录的iframe
    def open_iframe(self, a):
        return self.driver.switch_to.frame(a)

    # 切换回窗口的的content
    def switch_content(self):
        return self.driver.switch_to.default_content()

    # 清空内容
    def clear(self, locator):
        ele = self.findElement(locator)
        return ele.clear()

    # 判断网站title的方法
    def is_title(self, _title):
        """返回bool值 true&False"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_is(_title))
            return result
        except:
            return False

    # 读取csv文件
    def Get_Scv_Data(self, csv_file, line):
        logging.info("=====get_scv_data======")
        with open(csv_file, "r", encoding="utf-8-sig") as file:  # 防止出现非法字符使用sig方法
            reader = csv.reader(file)
            for index, row in enumerate(reader, 1):  # 需要获取到第几行的参数数据就改为几行
                if index == line:
                    return row

    # 判断网站title的方法,title过长时只要预期结果包含于实际结果的调用方法
    def is_title_contains(self, _title):
        """返回bool值 true&False"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(_title))
            return result
        except:
            return False

    # 判断元素文本相关的方法
    def text_in_element(self, locator, _text):
        """返回bool值 true&False,调用传参2个参数，元素和判断文本"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(
                EC.text_to_be_present_in_element(locator, _text))
            return result
        except:
            return False

    # 判断value值的方法
    def is_value_in_element(self, locator, _value):
        """返回bool值,value为空时返回false，获取value的方法是：get_attribute"""

        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(
                EC.text_to_be_present_in_element_value(locator, _value))
            return result
        except:
            return False

    # 判断是否出现alert弹窗
    def is_alert(self):
        """返回的是alert对象，确认返回后，可操作当前弹窗"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.alert_is_present())
            return result
        except:
            return False

    # 判断是否出现系统弹窗
    def is_alert_exist(self):
        """此处判断是否存在alert"""
        try:
            time.sleep(3)
            alert = self.driver.switch_to.alert
            text = alert.accept()
            return text
        except:
            return ""

    # 获取当前时间
    def getTime(self):
        return self.new

    # 截取当前页面图片
    def getScreenShot(self, module):
        Time = self.getTime()
        image_ile = os.path.dirname(os.path.dirname(__file__)) + '/Screenshot/%s_%s.png' % (module, Time)
        self.driver.get_screenshot_as_file(image_ile)

    # 鼠标悬停方法
    def move_to_element(self, locator):
        """鼠标移动悬停操作"""
        ele = self.findElement(locator)
        ActionChains(driver).move_to_element(ele).perform()

    # 页面选择下拉框通过索引来定位
    def select_by_index(self, locator, index=0):
        """通过索引，index是索引第几个，从0开始，默认选第一个"""
        element = self.findElement(locator)
        Select(element).select_by_index(index)

    # 页面选择下拉框通过value值来定位
    def select_by_value(self, locator, value):
        """通过value属性来判断"""
        element = self.findElement(locator)
        Select(element).select_by_value(value)

    # 页面选择下拉框通过value值来定位
    def select_by_text(self, locator, text):
        """通过文本定位"""
        element = self.findElement(locator)
        Select(element).select_by_visible_text(text)

    # 操作屏幕滚动条，当前页面元素不可见时需要调用此方法去滚动屏幕
    def js_scroll_end(self):
        """滚动到底部"""
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    def js_scroll_top(self):
        """回到顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    # 聚焦元素，在底部和顶部都无法看到元素时，我们久需要聚焦元素
    def js_focus_element(self, locator):
        """滚动到当前定位元素，注意在滚动需要点击的元素时，最好多留点空间，定位上面一点的元素，不然可能出现还是无法点击情况！！！"""
        target = self.findElement(locator)
        self.driver.execute_script("argument[0].scrollIntoView()", target)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://mail.qq.com/')
    boswer = Base(driver)
