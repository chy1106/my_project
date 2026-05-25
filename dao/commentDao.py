# _*_coding : utf-8 _*_
# @Time : 2026/3/2 21:14
# @File : commentDao
# @Project : weiboProject
'''
微博评论信息 数据访问对象
'''
from util import dbUtil

def getAllComment():
    '''
    获取所有评论信息
    :return:
    '''
    con = None
    try:
        con=dbUtil.getCon()
        cursor=con.cursor()
        sql="select * from t_comment where text_raw!=''"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getTopCommentUser():
    '''
    获取前50评论用户名
    :return:
    '''
    con = None
    try:
        con=dbUtil.getCon()
        cursor=con.cursor()
        sql="select username ,count(username) as unCount from t_comment GROUP BY username ORDER BY unCount DESC limit 0,50"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getCommentFenci():
    '''
    获取评论热词信息
    :return:
    '''
    con = None
    try:
        con=dbUtil.getCon()
        cursor=con.cursor()
        sql="select * from t_comment where text_raw!='' limit 0,100"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getCommentHotWordAmount(hotword):
    """
    获取日期用户热词评论量
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = f"SELECT DATE_FORMAT(created_at,'%Y-%m-%d') AS commentDate,COUNT(text_raw) AS commentTotal FROM t_comment WHERE LOCATE('{hotword}',text_raw)>0  GROUP BY commentDate ORDER BY commentDate DESC "
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getCommentByHotWord(hotword):
    """
    根据热词查询评论信息
    :return:
    """
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = f"SELECT * FROM t_comment WHERE LOCATE('{hotword}',text_raw)>0"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getAllSpecificComment():
    '''
    获取所有爬取评论信息
    :return:
    '''
    con = None
    try:
        con=dbUtil.getCon()
        cursor=con.cursor()
        sql="select * from s_comment where text_raw!=''"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getSpecificFenci():
    '''
    获取关键词评论分词信息
    :return:
    '''
    con = None
    try:
        con=dbUtil.getCon()
        cursor=con.cursor()
        sql="select * from s_comment where text_raw!=''"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)