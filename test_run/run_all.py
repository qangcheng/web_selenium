# coding=utf-8
"""
 r以读的方式打开文件，读取文件信息
 w 以写入当时打开文件，如果文件存在，清空文件重新写入
 a 以追加模式打开文件，可对文件进行读写操作
 w+ 消除文件内容，然后以读写方式打开
 a+ 以读写方式打开文件，并把文件指针移动到文件尾
 b 以二进制模式打开文件，不是文本模式
 测试报告加时间戳不利于持续集成，jenkins不能持续集成

"""


import unittest
from web_outo.common import HTMLTestRunner
import time
import logging
import logging.config
from os import path
import os


# 读取log.conf的配置表相关
log_file_path = os.path.dirname(os.path.dirname(__file__))+'/config/log.conf'
print(log_file_path)
logging.config.fileConfig(log_file_path)
logger = logging.getLogger()

# 用例路径
casePath = r'D:\web_pro\web_outo\case'
rule = "test*.py"

discover = unittest.defaultTestLoader.discover(start_dir=casePath, pattern=rule)

# 检查是否查到到用例
print(discover)
now = time.strftime("%Y-%m-%d %H_%M_%S")  # 加时间戳不利于持续集成，jenkins不能持续集成

reportpath = r"D:\\web_pro\\web_outo\\report\\" + now + "report.html"
fp = open(reportpath, "wb")


runer = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                      title="web自动化测试报告",
                                      description="XX项目自动化测试",
                                      )

runer.run(discover)
