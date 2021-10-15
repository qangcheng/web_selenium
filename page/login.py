from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from web_outo.common.base import Base


class Login_Ulis(Base):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    #  QQ 邮箱登录窗口元素
    switcher_plogin = (By.XPATH, '//*[@id="switcher_plogin"]')
    input_uesr = (By.ID, "u")
    input_password = (By.ID, "p")
    login_button = (By.ID, "login_button")

    # QQ未登录校验
    login_pictures = (By.CLASS_NAME, "login_pictures_title")

    # 本地已登录QQ
    def login(self, user, psw):
        self.open_iframe('login_frame')
        time.sleep(2)
        try:
            self.driver.find_element(*self.login_button)
        except NoSuchElementException:
            self.login_Two(user, psw)
        else:
            self.click(self.switcher_plogin)
            uesr = self.driver.find_element(*self.input_uesr)
            password = self.driver.find_element(*self.input_password)
            uesr.clear()
            password.clear()
            time.sleep(2)
            uesr.send_keys(user)
            password.send_keys(psw)
            time.sleep(2)
            self.driver.find_element(*self.login_button).click()
            time.sleep(5)
            self.switch_content()
            time.sleep(2)

    # 本地未登录QQ
    def login_Two(self, user, psw):
        self.open_iframe('login_frame')
        self.driver.find_element(*self.input_uesr).clear()
        self.driver.find_element(*self.input_password).clear()
        time.sleep(2)
        self.driver.find_element(*self.input_uesr).send_keys(user)
        self.driver.find_element(*self.input_password).send_keys(psw)
        time.sleep(2)
        self.driver.find_element(*self.login_button).click()
        time.sleep(5)
        self.switch_content()
        time.sleep(2)

    # link方法获取到当前页面的元素text文本来判定是否成功
    def get_login_uesrname(self, a):
        try:
            t = self.driver.find_element_by_link_text(a)
            return t.text
        except NoSuchElementException:
            return ""

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

    # 判断现弹窗
    def is_alert_confirm(self):
        try:
            # 切回系统弹窗
            time.sleep(3)
            confirm = self.driver.switch_to.confirm()
            text = confirm.text
            print(text)
            return text
        except:
            return ""


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://mail.qq.com/')
    login = Login_Ulis(driver)
    driver.maximize_window()
    login.login("1425000581", "weishi")
