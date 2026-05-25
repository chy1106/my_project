# _*_coding : utf-8 _*_
# @Time : 2026/2/25 18:45
# @File : article_spider
# @Project : weiboProject
import csv

import os
import time
from datetime import datetime

import requests

from util.stringUtil import clean_string

def clear_csv():
    with open("data/article_data.csv", 'w', encoding='utf8') as f:
        f.truncate()  # 直接截断文件内容

def init_csv():
    '''
    初始化操作，判断csv文件是否存在，不存在就创建
    :return:
    '''
    with open('data/article_data.csv', 'w',encoding='utf8',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id',#帖子id
            'text_raw',#内容
            'reposts_count',#转发总数
            'comments_count',#评论总数
            'attitudes_count',#点赞总数
            'region_name',#发布位置
            'created_at',#创建日期
            'articleType',#帖子类型
            'articleUrl',#帖子地址
            'authorId',#用户id
            'authorName',#用户名称
            'authorHomeUrl'#用户主页地址
        ])

def getJsonHtml(url,params,cookie):
    '''请求获取html内容，json格式'''
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'cookie': cookie,
        'referer':'https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https://weibo.com/'
    }
    response=requests.get(url=url,headers=headers,params=params)
    if response.status_code==200:
        return response.json()
    else:
        return None

def getAllTypeList():
    '''
    获取所有类别信息
    :return:
    '''
    allTypeList = []
    with open('data/arcType_data.csv', 'r', encoding='utf8', newline='') as file:
        reader=csv.reader(file)
        next(reader)
        for articleType in reader:
            allTypeList.append(articleType)
    return allTypeList

def writeToCsv(row):
    '''
    写入csv操作
    :param arcType:
    :return:
    '''
    with open('data/article_data.csv', 'a', encoding='utf8', newline='') as file:
        writer= csv.writer(file)
        writer.writerow(row)

def parseJson(json,articleType):
    '''
    解析json数据
    :param json:
    :return:
    '''
    articleList=json['statuses']
    for article in articleList:
        id=article['id']
        text_raw=clean_string(article['text_raw'])
        reposts_count=article['reposts_count']
        comments_count = article['comments_count']
        attitudes_count = article['attitudes_count']
        region_name=article.get('region_name','发布于').replace('发布于','').strip()
        created_at=datetime.strptime(article['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
        articleUrl='https://weibo.com/%s/%s'%(article['user']['id'],article['mblogid'])
        authorId=article['user']['id']
        authorName=article['user']['screen_name']
        authorHomeUrl='https://weibo.com/u/%s'%article['user']['id']
        writeToCsv([
            id,text_raw,reposts_count,comments_count,attitudes_count,region_name,created_at,articleType,articleUrl,authorId,authorName,authorHomeUrl
        ])

#读取cookie
def readCookie():
    with open('data/Cookie.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file)
        for cookie in reader:
            return cookie[0]

def start():
    clear_csv()
    cookie=readCookie()
    url='https://weibo.com/ajax/feed/hottimeline'
    init_csv()
    allTypeList=getAllTypeList()
    print("内容爬取开始")
    for articleType in allTypeList:
        print("爬取类型【%s】"% articleType[0])
        params={
            'group_id': articleType[1],
            'containerid': articleType[2],
            'extparam': 'discover|new_feed'
        }
        jsonHtml=getJsonHtml(url,params,cookie)
        parseJson(jsonHtml,articleType[0])
    print("内容爬取结束")

if __name__ == '__main__':
    start()