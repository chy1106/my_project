# _*_coding : utf-8 _*_
# @Time : 2026/3/6 09:48
# @File : articleDao
# @Project : weiboProject
'''
帖子数据访问对象
'''
from util import dbUtil

def getArticleByArcType(arcType):
    '''根据微博类型查询帖子信息'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql=f"select * from t_article where articleType='{arcType}'"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)



def getAllArticle():
    '''查询所有帖子信息'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql="select * from t_article limit 0,100"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getTotalArticle():
    '''获取帖子总数'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select count(*) from t_article"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getTopAuthor():
    '''获取点赞最高微博作者'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select authorName from t_article order by attitudes_count desc limit 0,1"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getTopRegion():
    '''获取点赞最高城市'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = "select region_name,sum(attitudes_count)AS ac from t_article where region_name!='' group by region_name order by ac desc limit 0,1"
        cursor.execute(sql)
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

def getArticleTopZan():
    '''获取点赞最高6条'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql="select text_raw,attitudes_count from t_article order by attitudes_count desc limit 0,6"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def get7DayArticle():
    '''获取最近7天帖子数量'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql="select DATE_FORMAT(created_at,'%Y-%m-%d') as articleDate,COUNT(text_raw) as articleTotal from t_article group by articleDate order by articleDate desc limit 0,7"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getArticleTypeAmount():
    '''获取帖子类别数量'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql="select articleType ,COUNT(articleType) from t_article GROUP BY articleType"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getAllSpecificArticle():
    '''查询所有帖子信息'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql="select * from s_article limit 0,20"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)