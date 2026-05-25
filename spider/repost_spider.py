# _*_coding : utf-8 _*_
# @Time : 2026/3/16 16:03
# @File : respost_spider
# @Project : weiboProject
import csv
import os
import time
from datetime import datetime

import requests

from util.stringUtil import clean_string

def clear_csv():
    with open("data/repost_data.csv", 'w', encoding='utf8') as f:
        f.truncate()  # 直接截断文件内容

def init_csv():
    '''
    初始化操作，判断csv文件是否存在，不存在就创建
    :return:
    '''
    with open('data/repost_data.csv', 'w',encoding='utf8',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'articleId',  # 微博id
            'text_raw',  # 评论内容
            'created_at',  # 创建日期
            'region_name',  # 发布位置
            'userId',  # 评论用户id
            'userName',  # 评论用户名称
            'userHomeUrl'  # 评论用户主页地址
        ])

def getJsonHtml(url,params,cookie):
    '''请求获取html内容，json格式'''
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'cookie': cookie,
        'referer':'https://weibo.com/1371701597/Qwcdptm4Z'
    }
    response=requests.get(url=url,headers=headers,params=params)
    if response.status_code==200:
        return response.json()
    else:
        return None

def writeToCsv(row):
    '''
    写入csv操作
    :param arcType:
    :return:
    '''
    with open('data/repost_data.csv', 'a', encoding='utf8', newline='') as file:
        writer= csv.writer(file)
        writer.writerow(row)

def parseJson(json,articleId):
    '''
    解析json数据
    :param json:
    :param articleId:
    :return:
    '''
    repostList=json['data']
    for repost in repostList:
        text_raw=clean_string(repost['text_raw'])
        created_at=datetime.strptime(repost['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
        region_name = repost.get('region_name', '发布于').replace('发布于', '').strip()
        userId=repost['user']['id']
        userName=repost['user']['screen_name']
        userHomeUrl='https://weibo.com/u/%s'%repost['user']['id']
        writeToCsv([
            articleId,text_raw, created_at,region_name,userId, userName,userHomeUrl
        ])



def getAllArticleList():
    '''
    获取所有信息
    :return:
    '''
    articleList = []
    with open('data/article_data.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for article in reader:
            articleList.append(article)
    return articleList

#读取cookie
def readCookie():
    with open('data/Cookie.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file)
        for cookie in reader:
            return cookie[0]

def start():
    cookie = readCookie()
    clear_csv()
    url='https://weibo.com/ajax/statuses/repostTimeline'
    init_csv()
    articleList = getAllArticleList()
    print("转发信息爬取开始")
    index=0
    for article in articleList:
        if index>=100:
            break
        print("正在爬取【%s】的转发信息"%article[1])
        params={
            'id':article[0],
            'page':1
        }
        jsonHtml= getJsonHtml(url,params,cookie)
        index=index+1
        if jsonHtml:
            parseJson(jsonHtml,article[0])
    print("转发信息爬取结束")

if __name__ == '__main__':
    start()