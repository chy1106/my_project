# _*_coding : utf-8 _*_
# @Time : 2026/2/3 22:27
# @File : arcType_spider
# @Project : weiboProject
'''
https://weibo.com/ajax/feed/allGroups
微博类别信息爬取 存csv文件
'''

import csv
import os
from urllib import response

import numpy as np
import requests


def init_csv():
    '''
    初始化操作，判断csv文件是否存在，不存在就创建
    :return:
    '''
    with open('data/arcType_data.csv', 'w',encoding='utf8',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            '类别标题',
            '分组id',
            '分类id',

        ])

def getJsonHtml(url,cookie):
    '''请求获取html内容，json格式'''
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'cookie': cookie,
        'referer':'https://weibo.com/?wvr=5'
    }
    response=requests.get(url=url,headers=headers)
    if response.status_code==200:
        return response.json()
    else:
        return None

def writeToCsv(arcType):
    '''
    写入csv操作
    :param arcType:
    :return:
    '''
    with open('data/arcType_data.csv', 'a', encoding='utf8', newline='') as file:
        writer= csv.writer(file)
        writer.writerow(arcType)



def parseJson(json):
    '''
    解析json数据
    :param json:
    :return:
    '''
    arcTypeList= np.append(json['groups'][3]['group'],json['groups'][4]['group'])
    print(arcTypeList)
    for arcType in arcTypeList:
        arcType_title=arcType['title']
        gid=arcType['gid']
        containerid=arcType['containerid']
        writeToCsv([arcType_title,gid,containerid])

#读取cookie
def readCookie():
    with open('data/Cookie.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file)
        for cookie in reader:
            return cookie[0]

def clear_csv():
    with open("data/arcType_data.csv", 'w', encoding='utf8') as f:
        f.truncate()  # 清理文件内容

def start():
    cookie = readCookie()
    clear_csv()
    init_csv()
    url='https://weibo.com/ajax/feed/allGroups'
    jsonhtml=getJsonHtml(url,cookie)

    parseJson(jsonhtml)


if __name__ == '__main__':
    start()
