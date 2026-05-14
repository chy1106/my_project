# _*_coding : utf-8 _*_
# @Time : 2026/3/18 14:10
# @File : specific_crawl
# @Project : weiboProject
from spider.specific_url_spider import start as urlcrawl
from spider.specific_article_spider import start as articlecrawl
from spider.specific_comment_spider import start as commentcrawl
from spider.sprcific_respost_spider import start as respostcrawl
from spider.save_specific_data import saveToDb as saveToDb


def start(keyword):
    print(keyword)
    print("文章url爬取开始")
    urlcrawl(keyword)
    print("文章url爬取结束")

    print("文章内容爬取开始")
    articlecrawl()
    print("文章内容爬取结束")

    print("文章评论爬取开始")
    commentcrawl()
    print("文章评论爬取结束")

    print("文章转发爬取开始")
    respostcrawl()
    print("文章转发爬取结束")

    print("保存数据开始")
    saveToDb()
    print("保存数据结束")

if __name__ == '__main__':
    keyword=None
    start(keyword)