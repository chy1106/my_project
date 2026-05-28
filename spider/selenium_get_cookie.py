# _*_coding : utf-8 _*_
# @Time : 2026/3/14 15:39
# @File : selenium_spider
# @Project : weiboProject
import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
driver = webdriver.Edge(options=edge_options)
'''微博登录网站'''
driver.get('https://passport.weibo.com/sso/signin')
cookieStr = driver.get_cookies()
oldCookie=cookieStr
while cookieStr==oldCookie:
    cookieStr = driver.get_cookies()
    #按cookie格式 定义目标顺序
    target_order = ['SCF', 'SUB', 'SUBP', 'ALF', 'XSRF-TOKEN', 'WBPSESS']
    #按照目标顺序筛选并排序cookie
    ordered_cookies = [cookie for cookie in cookieStr if cookie['name'] in target_order]
    ordered_cookies.sort(key=lambda x: target_order.index(x['name']))
    #生成格式化的cookie字符串
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in ordered_cookies])
    if cookie_string !="":
        with open('data/Cookie.csv', 'w', encoding='utf8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([cookie_string])