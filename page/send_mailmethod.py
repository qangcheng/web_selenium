# coding:utf-8

"""
编写人员：v_qangchen
Send_email(相当于公共类方法，发送邮件相关，注意后期参数实现配置化）
Send_mail_options（正常流程发送邮件）
Timed_sending（定时发送邮件）
注意！！！！ web自动化编写过程中一定要主要iframe和content的切换，当唯一元素无法定位时，首先排查是否涉及到iframe切换
定时发送弹窗相关的方法还未实现--待补充

"""

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from web_outo.page.login import Login_Ulis


class SendMail(Login_Ulis):
    # 收件人等信息输入相关元素
    composebtn = (By.ID, "composebtn")
    recipient = (By.XPATH, "//*[@id='toAreaCtrl']/div[2]/input")
    theme = (By.ID, "subject")
    text = (By.XPATH, "/html/body")

    # 发送按钮元素选项相关元素
    sendbutton = (By.NAME, "sendbtn")
    timebutton = (By.NAME, "timeSendbtn")
    yearsbutton = (By.CLASS_NAME, "ico_select_s")
    yeartext = (By.CLASS_NAME, "btn_select_txt")
    time_Send_button = (By.ID, "timeSend_QMDialog_confirm")
    Timedsending = (By.ID, "sendinfomsg")

    # 定时发送相关元素
    Gregorian_calendar = (By.XPATH, '//*[@id="timeSend_QMDialog_sendTimeType"]/label[2]')

    def Send_email(self, Recipient, theme, content):
        """邮件信息相关信息输入"""
        # 对比下封装与不封装的区别，提到代码运行稳定性，不用再去流程中sleep,代码简洁稳定
        # self.driver.find_element(*self.composebtn).click()
        self.click(self.composebtn)

        # 切换到收件人的iframe
        self.open_iframe("mainFrame")

        time.sleep(2)
        self.driver.find_element(*self.recipient).send_keys(Recipient)
        self.driver.find_element(*self.theme).send_keys(theme)

        # 切换到正文iframe
        self.open_iframe(self.driver.find_element_by_xpath('//*[@class="qmEditorIfrmEditArea"]'))
        try:
            # text_button = self.driver.find_element(*self.text)
            text_button = self.findElement(self.text)
        except NoSuchElementException as e:
            raise e
        else:
            text_button.click()
            time.sleep(2)
            text_button.send_keys(content)

            #  切回当前页面总体框架第一层，不是iframe页面
            self.switch_content()
            time.sleep(3)
            return True

    def Send_mail_options(self):
        """正常发送邮件"""

        # 切换到发送邮件相关操作页面
        self.open_iframe("mainFrame")
        try:
            send_button = self.driver.find_element(*self.sendbutton)
        except NoSuchElementException:
            return False
        else:
            send_button.click()
            self.switch_content()
            try:
                time.sleep(2)
                sendmail.open_iframe("mainFrame")
                t = self.driver.find_element_by_xpath('//*[@id="sendinfomsg"]').text
                self.getScreenShot(t)
                print(t)
                # 切回当前页面总体框架第一层，不是iframe页面
                self.switch_content()
                return True
            except NoSuchElementException:
                return False

    def Timed_sending(self):
        """ 定时发送邮件"""
        self.open_iframe("mainFrame")
        try:
            time_button = self.findElement(self.timebutton)
        except NoSuchElementException:
            return False
        else:
            time_button.click()
            time.sleep(3)
            self.switch_content()
            self.click(self.Gregorian_calendar)
            for i in range(2):
                self.click(self.yearsbutton)
            self.click(self.time_Send_button)
            # 页面刷新后记得查看切换当前在哪个框架中
            self.switch_content()
            try:
                # 页面刷新后记得查看切换当前在哪个框架中
                self.open_iframe("mainFrame")
                # 待补充弹窗操作相关方法
                pass
                t = self.findElement(self.Timedsending).text
                self.getScreenShot(t)
                print(t)
                return True
            except NoSuchElementException:
                return False

    def Save_draft(self):
        pass

    def Close_mail(self):
        pass

    def Mail_Send_Sucees(self, locator, _text):
        result = self.text_in_element(locator, _text)
        return result


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://mail.qq.com/')
    sendmail = SendMail(driver)
    sendmail.login("1425000581", "Weishi@321")
    time.sleep(2)
    sendmail.Send_email(Recipient="837050079@qq.com",
                        theme="这是一封测试邮件",
                        content=("hello word", "\nchenqiang"))
    # sendmail.Send_mail_options()
    sendmail.Timed_sending()
    time.sleep(2)
