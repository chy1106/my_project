# _*_coding : utf-8 _*_
# @Time : 2026/3/2 21:18
# @File : commentFenci
# @Project : weiboProject
'''微博评论信息分词，词频统计，写入csv'''
import re

import jieba
import pandas as pd

from dao import commentDao

def outCommentFreToCsv(sorted_wfc_list):
    '''
    词频统计写入csv
    :param sorted_wfc_list:
    :return:
    '''
    df=pd.DataFrame(sorted_wfc_list,columns=['热词','数量'])
    df.to_csv('fenci/comment_fre.csv',index=False)



def getStopWordList():
    '''
    获取停顿词
    '''
    return [line.strip() for line in open('fenci/stopWords.txt',encoding='utf-8').readlines()]


def cut_comment():
    '''
    分词
    :return:
    '''
    allComment=" ".join([comment[1].strip() for comment in commentDao.getCommentFenci()])
    print(allComment)
    seg_list= jieba.cut(allComment)
    return seg_list

def word_fre_count():
    '''
    词频统计，过滤数据，单个词及停顿词
    :return:
    '''
    seg_list=cut_comment()
    stopWordList=getStopWordList()
    '''正则去除数字、单字、停顿词'''
    new_seg_list=[]
    for seg in seg_list:
        number=re.search('\d+', seg)
        if not number and seg not in stopWordList and len(seg)>1:
            new_seg_list.append(seg)


    '''词频统计'''
    wfc={}
    for w in set(new_seg_list):
        wfc[w]=new_seg_list.count(w)
    print(wfc)

    sorted_wfc_list= sorted(wfc.items(), key=lambda x:x[1], reverse=True)
    return sorted_wfc_list

def start():
    cut_comment()
    getStopWordList()
    word_fre_count()
    outCommentFreToCsv(word_fre_count())

if __name__ == '__main__':

    start()
