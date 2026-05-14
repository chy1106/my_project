# _*_coding : utf-8 _*_
# @Time : 2026/3/15 20:59
# @File : repost_spider
# @Project : weiboProject
import csv
import os
from datetime import datetime
from urllib.parse import urlparse
import requests

from util.stringUtil import clean_string

def clear_csv():
    with open("data/specificArticle_data.csv", 'w', encoding='utf8') as f:
        f.truncate()  # 直接截断文件内容


def init_csv():
    '''
    初始化操作，判断csv文件是否存在，不存在就创建
    :return:
    '''

    with open('data/specificArticle_data.csv', 'w',encoding='utf8',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id',#帖子id
            'text_raw',#内容
            'reposts_count',#转发总数
            'comments_count',#评论总数
            'attitudes_count',#点赞总数
            'region_name',#发布位置
            'created_at',#创建日期
            'articleUrl',#帖子地址
            'authorId',#用户id
            'authorName',#用户名称
            'authorHomeUrl'#用户主页地址
        ])


def getAllArticleURLList():
    '''
    获取所有文章URL信息
    :return:
    '''
    allArticleURL = []
    with open('data/article_URL.csv', 'r', encoding='utf8', newline='') as file:
        reader=csv.reader(file)
        for article_url in reader:
            allArticleURL.append(article_url)
    return allArticleURL


def extract_target(url):
    # 解析URL并获取路径
    parsed = urlparse(url)
    path = parsed.path
    # 分割路径并过滤空段
    parts = [part for part in path.split('/') if part]
    # 返回最后一个有效段（若存在）
    return parts[-1] if parts else None


def getJsonHtml(refererUrl,urlRequest,cookie):
    '''请求获取html内容，json格式'''
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'cookie': cookie,
        'referer': 'https:' + refererUrl
    }

    response=requests.get(url=urlRequest,headers=headers)
    content = response.content.decode('utf-8')
    if response.status_code==200:
        return response.json()
    else:
        return None


def parseJson(jsonstr):
    '''
    解析json数据
    :param json:
    :return'''
    try:
        id=jsonstr['id']
        text_raw=clean_string(jsonstr['text_raw'])
        reposts_count=jsonstr['reposts_count']
        comments_count = jsonstr['comments_count']
        attitudes_count = jsonstr['attitudes_count']
        region_name=jsonstr.get('region_name','发布于').replace('发布于','').strip()
        created_at=datetime.strptime(jsonstr['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
        articleUrl='https://weibo.com/%s/%s'%(jsonstr['user']['id'],jsonstr['mblogid'])
        authorId=jsonstr['user']['id']
        authorName=jsonstr['user']['screen_name']
        authorHomeUrl='https://weibo.com/u/%s'%jsonstr['user']['id']
    except KeyError:
        return None  # 捕获异常后跳过

    writeToCsv([
        id,text_raw,reposts_count,comments_count,attitudes_count,region_name,created_at,articleUrl,authorId,authorName,authorHomeUrl
    ])




def writeToCsv(row):
    '''
    写入csv操作
    :param arcType:
    :return:
    '''
    with open('data/specificArticle_data.csv', 'a', encoding='utf8', newline='') as file:

        writer= csv.writer(file)
        writer.writerow(row)

def readCookie():
    with open('data/Cookie.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file)
        for cookie in reader:
            return cookie[0]

def start():
    cookie = readCookie()
    clear_csv()
    print("特定内容爬取开始")
    init_csv()
    ArticleUrlList= getAllArticleURLList()
    for ArticleUrl in ArticleUrlList:
        url= ArticleUrl[0]
        refererUrl=url.strip("[]")
        url1=extract_target(url)

        urlRequest='https://weibo.com/ajax/statuses/show?id='+url1+'&locale=zh-CN&isGetLongText=true'
        jsonhtml= getJsonHtml(refererUrl,urlRequest,cookie)
        parseJson(jsonhtml)

    print("特定内容爬取结束")


if __name__ == '__main__':
    start()
