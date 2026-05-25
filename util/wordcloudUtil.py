# _*_coding : utf-8 _*_
# @Time : 2026/3/11 15:26
# @File : wordcloudUtil
# @Project : weiboProject
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from wordcloud import WordCloud

def genWordCloudPic(str, outImg):
    """
    生成云图
    :param str: 词云 空格隔开
    :param outImg: 输出的词云图文件名
    :return:
    """
    wc = WordCloud(
        width=800,
        height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(str)
    # 绘制图片
    plt.imshow(wc)
    # 不显示坐标轴
    plt.axis('off')
    plt.savefig( './static/' + outImg, dpi=500)
