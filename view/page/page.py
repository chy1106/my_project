# _*_coding : utf-8 _*_
# @Time : 2026/2/3 22:14
# @File : page
# @Project : weiboProject
import os
import subprocess

import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from snownlp import SnowNLP
from flask_cors import CORS
from dao import articleDao, commentDao, repostDao
from spider import main
from spider.specific_crawl import  start as specificCrawl
from fenci.commentFenci import start as startFenci
from fenci.specificCommentFenci import start as keywordFenci


from util import wordcloudUtil

pb=Blueprint('page',__name__,url_prefix='/page',template_folder='templates')
CORS(pb)
@pb.route('/home')
def home():
    '''进入页面，获取相应数据'''
    articleData=articleDao.get7DayArticle()
    '''x轴'''
    xAxis7ArticleData=[]
    '''y轴'''
    yAxis7ArticleData=[]
    for article in articleData:
        xAxis7ArticleData.append(article[0])#日期
        yAxis7ArticleData.append(article[1])#数据

    '''获取帖子类别数量'''
    arcTypeData=[]
    articleTypeAmountList=articleDao.getArticleTypeAmount()
    for arcType in articleTypeAmountList:
        arcTypeData.append({'value': arcType[1], 'name': arcType[0]})

    '''获取top50评论用户名'''
    top50CommentUserList= commentDao.getTopCommentUser()
    '''只取name'''
    top50CommentUserNameList=[cu[0] for cu in top50CommentUserList]
    str=' '.join(top50CommentUserNameList)
    wordcloudUtil.genWordCloudPic(str,'comment_user_cloud.jpg')

    return render_template('index.html',
                           xAxis7ArticleData=xAxis7ArticleData,
                           yAxis7ArticleData=yAxis7ArticleData,
                           arcTypeData=arcTypeData)

@pb.route('/homePageData')
def getHomePageData():
    '''获取主页数据 ajax异步交互'''
    totalArticle= articleDao.getTotalArticle()
    topAuthor= articleDao.getTopAuthor()
    topRegion= articleDao.getTopRegion()
    topArticles= articleDao.getArticleTopZan()
    return jsonify(totalArticle=totalArticle,topAuthor=topAuthor,topRegion=topRegion,topArticles=topArticles)

@pb.route('/hotWord')
def hotWord():
    '''热词分析统计'''
    hotwordList = []
    # 只读取前100条
    df = pd.read_csv('./fenci/comment_fre.csv', nrows=100)
    for value in df.values:
        hotwordList.append(value[0])
    # 获取请求参数，如果没有获取到，给个默认值 第一个列表数据
    defaultHotWord = request.args.get('word', default=hotwordList[0])
    hotwordNum = 0  # 出现次数
    for value in df.values:
        if defaultHotWord == value[0]:
            hotwordNum = value[1]
    # 情感分析
    sentiments = ''
    stc = SnowNLP(defaultHotWord).sentiments
    if stc > 0.6:
        sentiments = '正面'
    elif stc < 0.2:
        sentiments = '负面'
    else:
        sentiments = '中性'

    commentHotWordData = commentDao.getCommentHotWordAmount(defaultHotWord)
    xAxisHotWordData = []
    yAxisHotWordData = []
    for comment in commentHotWordData:
        xAxisHotWordData.append(comment[0])
        yAxisHotWordData.append(comment[1])

    commentList = commentDao.getCommentByHotWord(defaultHotWord)
    return render_template('hotWord.html',
                           hotwordList=hotwordList,
                           defaultHotWord=defaultHotWord,
                           hotwordNum=hotwordNum,
                           sentiments=sentiments,
                           xAxisHotWordData=xAxisHotWordData,
                           yAxisHotWordData=yAxisHotWordData,
                           commentList=commentList)


@pb.route('/articleData')
def articleData():
    '''微博舆情分析'''
    articleOldList=articleDao.getAllArticle()
    articleNewList=[]
    for article in articleOldList:
        article=list(article)
        sentiments = ''
        if article and article[1]:  # 确保article存在且content非空
            stc = SnowNLP(article[1]).sentiments
        else:
            stc = 0.5  # 默认中性情感值，或根据业务需求调整
        if stc > 0.6:
            sentiments = '正面'
        elif stc < 0.2:
            sentiments = '负面'
        else:
            sentiments = '中性'
        article.append(sentiments)
        articleNewList.append(article)
    return render_template('articleData.html',articleList=articleNewList)


@pb.route('/articleDataAnalysis')
def articleDataAnalysis():
    '''微博数据分析'''
    arcTypeList=[]
    df= pd.read_csv('./data/arcType_data.csv')
    for value in df.values:
        arcTypeList.append(value[0])
    # 获取请求参数，如果没有获取到，给个默认值第一个列表数据
    defaultArcType = request.args.get('arcType', default=arcTypeList[0])
    print(defaultArcType)
    articleList = articleDao.getArticleByArcType(defaultArcType)
    xZfData = []  # 转发x轴数据
    rangeNum = 1000
    rangeNum2 = 100
    for item in range(0, 20):
        xZfData.append(str(rangeNum2 * item) + '-' + str(rangeNum2 * (item + 1)))
    xZfData.append('2千+')
    yZfData=[0 for x in range(len(xZfData))]#转发y轴数据
    # 统计数据
    for article in articleList:
        for item in range(len(xZfData)):
            if int(article[2]) < rangeNum2 * (item + 1):
                yZfData[item] += 1
                break
            elif int(article[2]) > 2000:
                yZfData[len(xZfData) - 1] += 1
                break
    return render_template('articleDataAnalysis.html',
                           arcTypeList=arcTypeList,
                           defaultArcType=defaultArcType,
                           xZfData=xZfData,
                           yZfData=yZfData)


@pb.route('/repostAnalysis')
def repostAnalysis():
     #获取请求参数，如果没有获取到，给个默认值第一个列表数据
     ArcType = request.args.get('arcType', default='热门')
     print(ArcType)
     #转发路径图
     route=repostDao.getRepost(ArcType)
     print(route)
     return route



@pb.route('/commentDataAnalysis')
def commentDataAnalysis():
    '''
    微博评论数据分析
    :return:
    '''
    startFenci()
    commentList= commentDao.getAllComment()
    xDzData=[]#点赞x轴数据
    rangeNum=5
    for item in range(0,20):
        xDzData.append(str(rangeNum*item)+'-'+str(rangeNum*(item+1)))
    xDzData.append('1百+')
    yDzData=[0 for x in range(len(xDzData))]#点赞y轴数据
    #定义性别字典
    genderDic={'男':0,'女':0}
    for comment in commentList:
        for item in range(len(xDzData)):
            if int(comment[4])< rangeNum *(item+1):
                yDzData[item]+=1
                break
            elif int(comment[4])>100:
                #最后一个
                yDzData[len(xDzData)-1]+=1
                break
            if genderDic.get(comment[8],-1)!=-1:
                genderDic[comment[8]]+=1
    #性别数据
    genderData=[{'name':x[0],'value':x[1]}for x in genderDic.items()]
    #读取前50条数据
    df= pd.read_csv('./fenci/comment_fre.csv',nrows=100)
    hotCommentWordList =[x[0] for x in df.values]
    str2=' '.join(hotCommentWordList)
    wordcloudUtil.genWordCloudPic(str2,'comment_cloud.jpg')
    return render_template('commentDataAnalysis.html',
                           xDzData=xDzData,
                           yDzData=yDzData,
                           genderData=genderData)



@pb.route('/weiboLogin', methods=[ 'GET','POST'])
def run_selenium():
    if request.method == 'GET':
        return render_template('Sindex.html')
    script_path = os.path.abspath('./spider/selenium_get_cookie.py')
    if not os.path.exists(script_path):
        return jsonify({'status': 'error', 'message': '脚本文件不存在'}), 400
    command = ['python', script_path]
    result = subprocess.run(
        command,
        text=True,
    )
    return jsonify({
        'status': 'success' if result.returncode == 0 else 'error',
        'error': result.stderr
    })


@pb.route('/hotSpider',methods=[ 'GET','POST'])
def run_hotSpider():
    main.start()
    return ''


@pb.route('/crawl', methods=['GET','POST'])
def scrape_keyword():
    """接收前端发送的关键词并启动爬虫"""
    try:
        # 获取前端发送的JSON数据
        data = request.get_json()
        #从JSON中获取关键词
        keyword = data.get('keyword')
        if not keyword:
            return jsonify({
                'success': False,
                'message': '关键词不能为空'
            }), 400
        print(f"接收到关键词: {keyword}")

        specificCrawl(keyword)
        # 返回成功响应
        return jsonify({
            'success': True,
            'message': f'成功接收关键词: {keyword}',

        })

    except Exception as e:
        print(f"处理请求时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500




@pb.route('/specificArticleData')
def specificArticleData():
    '''微博文章舆情分析'''
    articleOldList=articleDao.getAllSpecificArticle()
    articleNewList=[]
    for article in articleOldList:
        article=list(article)
        sentiments = ''
        if article and article[1]:  # 确保article存在且content非空
            stc = SnowNLP(article[1]).sentiments
        else:
            stc = 0.5  # 默认中性情感值，或根据业务需求调整
        if stc > 0.6:
            sentiments = '正面'
        elif stc < 0.2:
            sentiments = '负面'
        else:
            sentiments = '中性'
        article.append(sentiments)
        articleNewList.append(article)
    return render_template('specificArticleData.html',articleList=articleNewList)


@pb.route('/specificCommentData')
def specificCommentData():
    '''微博文章评论分析'''
    keywordFenci()
    commentOldList=commentDao.getAllSpecificComment()
    commentNewList=[]

    # 定义性别字典
    genderDic = {'男': 0, '女': 0}


    for comment in commentOldList:

        comment=list(comment)
        sentiments = ''
        if genderDic.get(comment[8], -1) != -1:
            genderDic[comment[8]] += 1

        if comment and comment[1]:  # 确保article存在且content非空
            stc = SnowNLP(comment[1]).sentiments
        else:
            stc = 0.5  # 默认中性情感值，或根据业务需求调整
        if stc > 0.6:
            sentiments = '正面'
        elif stc < 0.2:
            sentiments = '负面'
        else:
            sentiments = '中性'
        comment.append(sentiments)
        commentNewList.append(comment)

    # 性别数据
    genderData = [{'name': x[0], 'value': x[1]} for x in genderDic.items()]
    # 读取前50条数据
    df = pd.read_csv('./fenci/specificComment_fre.csv', nrows=100)
    hotCommentWordList = [x[0] for x in df.values]
    str2 = ' '.join(hotCommentWordList)
    wordcloudUtil.genWordCloudPic(str2, 's_comment_cloud.jpg')
    return render_template('specificCommentData.html',commentList=commentNewList,genderData=genderData)



@pb.route('/specificRepostData')
def specificRepostData():
    #微博转发数据
    repostList = repostDao.getRepostData()
    print(repostList)
    return render_template('repostRouteAnalysis.html',repostList=repostList)


@pb.route('/repostRouteAnalysis')
def repostRouteAnalysis():
    #转发路径图
    route=repostDao.getRepostRoute()
    print(route)
    return route