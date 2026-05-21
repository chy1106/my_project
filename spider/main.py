# _*_coding : utf-8 _*_
# @Time : 2026/3/2 09:42
# @File : main
# @Project : weiboProject

'''
爬取数据，持久化到数据库
'''
import traceback

import pandas as pd
from sqlalchemy import create_engine
from spider.arcType_spider import start as typespiderStart
from spider.article_spider import start as articlespiderStart
from spider.comment_spider import start as commentspiderStart
from spider.repost_spider import start as repostspiderStart

engine=create_engine('mysql+pymysql://root:123456@localhost:3306/weibo?charset=utf8')
'''
持久化到数据库，先合并数据库和csv文件，去重，最后存数据库，删除csv文件
:return:
'''
def saveToDb():
    try:
        '''帖子'''
        oldArticleDb= pd.read_sql('select* from t_article',engine)
        newArticleCsv = pd.read_csv('data/article_data.csv')
        '''合并'''
        concatArticlePd= pd.concat([newArticleCsv, oldArticleDb])
        '''id去重'''
        resultArticlePd=concatArticlePd.drop_duplicates(subset='id',keep='last')
        '''存库'''
        resultArticlePd.to_sql('t_article',con=engine,if_exists='replace',index=False)

        '''评论'''
        oldCommentDb = pd.read_sql('select* from t_comment', engine)
        newCommentCsv = pd.read_csv('data/comment_data.csv')
        '''合并'''
        concatCommentPd = pd.concat([newCommentCsv, oldCommentDb])
        '''id去重'''
        resultCommentPd = concatCommentPd.drop_duplicates(subset='id', keep='last')
        '''存库'''
        resultCommentPd.to_sql('t_comment', con=engine, if_exists='replace', index=False)

        '''转发'''
        oldRepostDb = pd.read_sql('select* from t_repost', engine)
        newRepostCsv = pd.read_csv('data/repost_data.csv')
        '''合并'''
        concatRepostPd = pd.concat([newRepostCsv, oldRepostDb])
        '''id去重'''
        resultRepostPd = concatRepostPd.drop_duplicates(subset='articleId', keep='last')
        '''存库'''
        resultRepostPd.to_sql('s_repost', con=engine, if_exists='replace', index=False)
    except Exception as e:
        print("异常",e)
        traceback.print_exc()
        newArticleCsv= pd.read_csv('data/article_data.csv')
        newCommentCsv= pd.read_csv('data/comment_data.csv')
        newRepostCsv= pd.read_csv('data/repost_data.csv')
        newArticleCsv.to_sql('t_article',con=engine,if_exists='replace',index=False)
        newCommentCsv.to_sql('t_comment',con=engine,if_exists='replace',index=False)
        newRepostCsv.to_sql('t_repost',con=engine,if_exists='replace',index=False)

def start():
    print("热词爬取开始")
    typespiderStart()
    print("热词爬取结束")
    print("内容爬取开始")
    articlespiderStart()
    print("内容爬取结束")
    print("评论爬取开始")
    commentspiderStart()
    print("评论爬取结束")
    print("转发爬取开始")
    repostspiderStart()
    print("转发爬取结束")
    print("持久化开始")
    saveToDb()
    print("持久化结束")

if __name__ == '__main__':
    start()