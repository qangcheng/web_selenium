"""
os.path.realpath(__file__))：获取到脚本当前真实路径
os.path.dirname(os.path.realpath(__file__))：获取到当前脚本的上一层目录，以此类推，有多少层，再加一个os.path.dirname包含里面，找到工程第一个路径为止
os.path.join：添加路径链接（propath, "data", "account.csv"）
如果propath指向地址为C:\\,再加上后面2个参数打印出来的地址就是：C:\\data\\account.csv


"""


import os
import time
import logging
from os import path
import logging.config
module = "wewewe"
Time= time.strftime("%Y-%m-%d %H_%M_%S")
image_ile = os.path.dirname(os.path.dirname(__file__)) + '/Photo_screenshot/%s_%s.png' % (module, Time)
print(image_ile)


propath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
filepath = os.path.join(propath, "data", "account.csv")
print(filepath)
