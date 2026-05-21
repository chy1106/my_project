# _*_coding : utf-8 _*_
# @Time : 2026/2/28 21:53
# @File : comment_spider
# @Project : weiboProject
'''
爬取评论
'''
import csv
import os
import time
from datetime import datetime

import requests

from spider.arcType_spider import getJsonHtml
from util.stringUtil import clean_string



def clear_csv():
    with open("data/comment_data.csv", 'w', encoding='utf8') as f:
        f.truncate()  # 直接截断文件内容

def init_csv():
    '''
    初始化操作，判断csv文件是否存在，不存在就创建
    :return:
    '''
    with open('data/comment_data.csv', 'w',encoding='utf8',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id',  # 评论信息id
            'text_raw',  # 评论内容
            'created_at',  # 创建日期
            'source',  # 发布位置 少部分没有这个值
            'like_counts',  # 点赞数
            'articleId',  # 微博id
            'userId',  # 评论用户id
            'userName',  # 评论用户名称
            'gender',  # 性别
            'userHomeUrl'  # 评论用户主页地址
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

def writeToCsv(row):
    '''
    写入csv操作
    :param arcType:
    :return:
    '''
    with open('data/comment_data.csv', 'a', encoding='utf8', newline='') as file:
        writer= csv.writer(file)
        writer.writerow(row)

def parseJson(json,articleId):
    '''
    解析json数据
    :param json:
    :param articleId:
    :return:
    '''
    commentList=json['data']
    for comment in commentList:
        id=comment['id']
        text_raw=clean_string(comment['text_raw'])
        created_at=datetime.strptime(comment['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
        source=comment.get('source','来自').replace('来自','').strip()
        like_counts=comment['like_counts']
        userId=comment['user']['id']
        userName=comment['user']['screen_name']
        gender='男'
        g=comment['user']['gender']
        if g=='f':
            gender='女'
        userHomeUrl='https://weibo.com/u/%s'%comment['user']['id']
        writeToCsv([
            id, text_raw, created_at,source,like_counts,articleId,userId, userName,gender,userHomeUrl
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
    clear_csv()
    cookie=readCookie()
    url='https://weibo.com/ajax/statuses/buildComments'
    init_csv()
    articleList = getAllArticleList()
    print("评论信息爬取开始")
    index=1
    for article in articleList:
        if index<=50:
            index=index+1
            print("正在爬取标题为：【%s】的微博评论"%article[1])
            time.sleep(1)
            params={
                'id':article[0],
                'is_show_bulletin':2
            }
            jsonHtml= getJsonHtml(url,params,cookie)
            if jsonHtml:
                parseJson(jsonHtml,article[0])
    print("评论信息爬取结束")

if __name__ == '__main__':
    start()