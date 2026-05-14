# _*_coding : utf-8 _*_
# @Time : 2026/3/16 09:50
# @File : save_specific_data
# @Project : weiboProject
import os
import traceback

import pandas as pd
from sqlalchemy import create_engine

engine=create_engine('mysql+pymysql://root:123456@localhost:3306/weibo?charset=utf8')

def saveToDb():
    '''
    持久化到数据库，先合并数据库和csv文件，去重，最后存数据库，删除csv文件
    :return:
    '''

    newArticleCsv= pd.read_csv('data/specificArticle_data.csv')
    newCommentCsv= pd.read_csv('data/specificComment_data.csv')
    newRepostCsv= pd.read_csv('data/specificRepost_data.csv')
    newArticleCsv.to_sql('s_article',con=engine,if_exists='replace',index=False)
    newCommentCsv.to_sql('s_comment',con=engine,if_exists='replace',index=False)
    newRepostCsv.to_sql('s_repost',con=engine,if_exists='replace',index=False)


if __name__ == '__main__':
    saveToDb()