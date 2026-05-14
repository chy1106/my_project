# _*_coding : utf-8 _*_
# @Time : 2026/3/2 21:11
# @File : dbUtil
# @Project : weiboProject

from pymysql import Connection

def getCon():
    '''
    获取数据连接
    :return:
    '''
    con=Connection(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        database='weibo',
        autocommit=True
    )
    return con

def closeCon(con: Connection):
    '''
    关闭数据库连接
    :param con:
    :return:
    '''
    if con:
        con.close()