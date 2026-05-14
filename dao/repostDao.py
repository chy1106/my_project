# _*_coding : utf-8 _*_
# @Time : 2026/3/23 12:14
# @File : repostDao
# @Project : weiboProject
from flask import request

from entity.UserModel import User
from util import dbUtil

def getRepost(articleType):
    '''查询转发路径'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()

        sql = (f"select t_article.region_name as source,t_repost.region_name as target,"
               f"count(*)as VALUE from t_article JOIN t_repost on t_article.id=t_repost.articleId "
               f"where t_article.region_name is not NULL and t_repost.region_name is not NULL "
               f"and t_repost.region_name!=t_article.region_name "
               f"and t_article.articleType = %s"
               f"GROUP BY t_article.region_name,t_repost.region_name")
        cursor.execute(sql, (articleType,))
        rows= cursor.fetchall()
        geo_coord_map = {
            "北京": [116.40, 39.90], "上海": [121.47, 31.23], "天津": [117.20, 39.08], "重庆": [106.55, 29.56],
             "河北": [114.50, 38.00], "河南": [113.60, 34.76], "云南": [102.70, 25.00], "辽宁": [123.40, 41.80],
             "黑龙江": [126.60, 45.75], "湖南": [113.00, 28.00], "安徽": [117.20, 31.80], "山东": [117.00, 36.65],
             "新疆": [87.60, 43.80], "江苏": [118.78, 32.07], "浙江": [120.15, 30.28], "江西": [115.89, 28.68],
            "湖北": [114.31, 30.52], "广西": [108.30, 22.80], "甘肃": [103.80, 36.05], "山西": [112.50, 37.85],
             "内蒙古": [111.65, 40.80], "陕西": [108.93, 34.34], "吉林": [125.30, 43.90], "福建": [119.30, 26.08],
             "贵州": [106.70, 26.57], "广东": [113.23, 23.16], "青海": [101.70, 36.56], "西藏": [91.11, 29.97],
             "四川": [104.06, 30.67], "宁夏": [106.20, 38.47], "海南": [110.35, 20.02], "中国台湾": [121.50, 25.00],
             "中国香港": [114.17, 22.28], "中国澳门": [113.54, 22.19]
        }
        nodes_set = set()  # 用集合去重
        edges = []
        for row in rows:
            source = row[0]
            target = row[1]
            count_val = row[2]
            #只保留有坐标的地区
            if source not in geo_coord_map or target not in geo_coord_map:
                continue
            # 添加到节点集合
            nodes_set.add(source)
            nodes_set.add(target)
            # 添加到边列表
            edges.append({
                "source": source,
                "target": target,
                "value": count_val
            })
        nodes = [{"name": name, "value": geo_coord_map[name]} for name in nodes_set]
        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)



def getRepostData():
    '''查询转发信息'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql=(f"select s_article.id as id,s_article.authorName as authorname, s_repost.userName as username,"
             f"s_article.region_name as source,s_repost.region_name as target,"
             f"count(*)as VALUE from s_article JOIN s_repost on s_article.id=s_repost.articleId "
             f"where s_article.region_name is not NULL and s_repost.region_name is not NULL "
             f"and s_repost.region_name!=s_article.region_name "
             f"GROUP BY s_article.id, s_article.authorName ,s_article.region_name,s_repost.region_name,s_repost.userName")
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)


def getRepostRoute():
    '''查询转发路径'''
    con = None
    try:
        con = dbUtil.getCon()
        cursor = con.cursor()
        sql = (f"select s_article.region_name as source,s_repost.region_name as target,"
               f"count(*)as VALUE from s_article JOIN s_repost on s_article.id=s_repost.articleId "
               f"where s_article.region_name is not NULL and s_repost.region_name is not NULL "
               f"and s_repost.region_name!=s_article.region_name "
               f"GROUP BY s_article.region_name,s_repost.region_name")
        cursor.execute(sql)
        rows= cursor.fetchall()
        geo_coord_map = {
            "北京": [116.40, 39.90], "上海": [121.47, 31.23], "天津": [117.20, 39.08], "重庆": [106.55, 29.56],
             "河北": [114.50, 38.00], "河南": [113.60, 34.76], "云南": [102.70, 25.00], "辽宁": [123.40, 41.80],
             "黑龙江": [126.60, 45.75], "湖南": [113.00, 28.00], "安徽": [117.20, 31.80], "山东": [117.00, 36.65],
             "新疆": [87.60, 43.80], "江苏": [118.78, 32.07], "浙江": [120.15, 30.28], "江西": [115.89, 28.68],
            "湖北": [114.31, 30.52], "广西": [108.30, 22.80], "甘肃": [103.80, 36.05], "山西": [112.50, 37.85],
             "内蒙古": [111.65, 40.80], "陕西": [108.93, 34.34], "吉林": [125.30, 43.90], "福建": [119.30, 26.08],
             "贵州": [106.70, 26.57], "广东": [113.23, 23.16], "青海": [101.70, 36.56], "西藏": [91.11, 29.97],
             "四川": [104.06, 30.67], "宁夏": [106.20, 38.47], "海南": [110.35, 20.02], "中国台湾": [121.50, 25.00],
             "中国香港": [114.17, 22.28], "中国澳门": [113.54, 22.19]
        }
        nodes_set = set()  #用集合去重
        edges = []
        for row in rows:
            source = row[0]
            target = row[1]
            count_val = row[2]
            #只保留有坐标的地区
            if source not in geo_coord_map or target not in geo_coord_map:
                continue
            # 添加到节点集合
            nodes_set.add(source)
            nodes_set.add(target)
            # 添加到边列表
            edges.append({
                "source": source,
                "target": target,
                "value": count_val
            })
        nodes = [{"name": name, "value": geo_coord_map[name]} for name in nodes_set]
        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)