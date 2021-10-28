# coding:utf-8

"""
编写人员：v_QiangChen（丁钢平的爸爸）
封装所有元素可能实现得动作，代码相比send_mailmethod.py更加明了简洁，但是send_mailmethod.py实现了整个流程，调用
就需要固定流程得需求，如果需要调用单一功能APIsendmailpage更加轻量化，但需要自己在调试出写流程代码
注意！！！！ web自动化编写过程中一定要主要iframe和content的切换，当唯一元素无法定位时，首先排查是否涉及到iframe切换
定时发送弹窗相关的方法还未实现--待补充
切记页面跳转增加timesleep等待页面加载完成后再开始定位！！！！

"""

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from web_outo.page.login_page import Login


class SendMail(Login):
    # 收件人等信息输入相关元素
    composebtn = (By.ID, "composebtn")
    recipient = (By.XPATH, "//*[@id='toAreaCtrl']/div[2]/input")
    theme = (By.ID, "subject")
    text = (By.XPATH, "/html/body")

    # 发送按钮元素选项相关元素
    sendbutton = (By.NAME, "sendbtn")
    yeartext = (By.CLASS_NAME, "btn_select_txt")
    Back_button = (By.PARTIAL_LINK_TEXT, "返回邮箱首页")
    Mail_sent_successfully = (By.XPATH, '//*[@id="sendinfomsg"]')

    # 定时发送相关元素
    timebutton = (By.NAME, "timeSendbtn")
    Gregorian_calendar = (By.XPATH, '//*[@id="timeSend_QMDialog_sendTimeType"]/label[2]')
    yearsbutton = (By.CLASS_NAME, "ico_select_s")
    time_Send_button = (By.ID, "timeSend_QMDialog_confirm")
    Timedsending = (By.ID, "sendinfomsg")

    def Click_Write_entry(self):
        """点击写信入口"""
        self.click(self.composebtn)

    def Input_Recipient(self, Recipient="837050079@qq.com"):
        """输入收件人信息"""
        self.open_iframe("mainFrame")  # 收件人信息页面需要切换iframe
        self.sendKeys(self.recipient, Recipient)
        self.switch_content()  # 切换到主框架

    def input_Theme(self, theme="这是一封测试邮件"):
        """输入主题信息"""
        self.open_iframe("mainFrame")  # 收件人信息页面需要切换iframe
        self.sendKeys(self.theme, theme)
        self.switch_content()  # 切换到主框架

    def Input_The_Text(self, content=("hello word", "\nchenqiang")):
        """输入正文信息"""
        # 首先需要切换到正文得iframe
        self.open_iframe("mainFrame")
        self.open_iframe(self.driver.find_element_by_xpath('//*[@class="qmEditorIfrmEditArea"]'))
        self.click(self.text)
        self.sendKeys(self.text, content)
        self.switch_content()  # 切换到主框架

    def Send_mail_options(self):
        """点击发送邮件按钮"""
        self.open_iframe("mainFrame")  # 切换iframe
        self.click(self.sendbutton)
        self.switch_content()  # 切换到主框架

    def Return_to_mailbox_homepage(self):
        """点击返回邮箱首页"""
        self.open_iframe("mainFrame")
        self.click(self.Back_button)
        time.sleep(2)
        self.switch_content()
        self.getScreenShot("返回首页")

    def Click_Timed_send_button(self):
        """选择定时发送按钮渠道的按钮"""
        self.open_iframe("mainFrame")  # 切换iframe
        self.click(self.timebutton)
        self.switch_content()  # 切换到主框架

    def Click_Year_button(self):
        """点击年份按钮"""
        self.switch_content()
        self.click(self.yearsbutton)

    def Click_time_Send_button(self):
        """点击定时发送按钮"""
        self.switch_content()
        self.click(self.time_Send_button)

    def Send_Mail(self):
        """常规正常发送邮件"""
        self.Click_Write_entry()
        self.Input_Recipient()
        self.input_Theme()
        self.Input_The_Text()
        self.Send_mail_options()
        self.Send_mail_successfully()
        self.Return_to_mailbox_homepage()

    def Send_mail_regularly(self):
        """定时发送邮件"""
        self.Click_Write_entry()
        self.Input_Recipient()
        self.input_Theme()
        self.Input_The_Text()
        self.Click_Timed_send_button()
        for i in range(2):
            self.Click_Year_button()
        self.Click_time_Send_button()
        # self.Timedsending_emailpage_verification()
        # self.Return_to_mailbox_homepage()

    def Send_mail_successfully(self):
        """判断正常发送登录页面是否出现该元素，做校验用"""
        # 出现跳转页面时，最好等待3秒，待所有加载完成后再去定位，不然会报错
        time.sleep(3)
        self.open_iframe("mainFrame")
        try:
            t = self.findElement(self.Mail_sent_successfully)
            self.getScreenShot("邮件发送成功")
            print(t.text)
            self.switch_content()
            return True
        except NoSuchElementException:
            return False

    def Timedsending_emailpage_verification(self):
        """判断定时发送发送登录页面是否出现该元素，做校验用"""
        # 出现跳转页面时，最好等待3秒，待所有加载完成后再去定位，不然会报错
        time.sleep(3)
        self.open_iframe("mainFrame")
        try:
            t = self.findElement(self.Timedsending).text
            self.getScreenShot(t)
            print(t)
            self.switch_content()
            return True
        except NoSuchElementException:
            return False


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://mail.qq.com/')
    sendmail = SendMail(driver)
    sendmail.login_QQ(autologin_button=True)
    sendmail.Send_Mail()
    # sendmail.Send_mail_regularly()
