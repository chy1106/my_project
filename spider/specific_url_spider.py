# _*_coding : utf-8 _*_
# @Time : 2026/3/14 18:05
# @File : test
# @Project : weiboProject
import csv
import os
from bs4 import BeautifulSoup
import requests

#清空article_URL.csv文件中所有内容
def clear_csv():
    with open("data/article_URL.csv", 'w', encoding='utf8') as f:
        f.truncate()

def init_csv():
    '''
    初始化操作，判断csv文件是否存在，不存在就创建
    :return:
    '''
    if not os.path.exists("data/article_URL.csv"):
        with open('data/article_URL.csv', 'w',encoding='utf8',newline='') as file:
            csv.writer(file)

def writeToCsv(url):
    '''
    写入csv操作
    '''
    with open('data/article_URL.csv', 'a', encoding='utf8', newline='') as file:
        writer= csv.writer(file)
        writer.writerow([url])

def readCookie():
    with open('data/Cookie.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file)
        for cookie in reader:
            return cookie[0]

def start(keyword):
    print(keyword)
    cookie= readCookie()
    clear_csv()
    url = 'https://s.weibo.com/weibo?q=' + keyword
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'cookie': cookie,
        'referer': 'https://weibo.com/'
    }
    response = requests.get(url=url, headers=headers)
    page = BeautifulSoup(response.content.decode('utf-8','ignore'), 'html.parser')
    url_list = page.find_all('div', attrs={'class': 'from'})
    init_csv()
    for url in url_list:
        #使用beautifulsoup从url中提取<a>标签内容
        a=url.find('a')
        #使用beautifulsoup从url中提取<a href="">标签的href内容
        article_url=a.get("href")
        writeToCsv(article_url)
        print(article_url)

if __name__ == '__main__':
    keyword=None
    start(keyword)


