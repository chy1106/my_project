# _*_coding : utf-8 _*_
# @Time : 2026/2/25 19:20
# @File : stringUtil
# @Project : weiboProject
import re

def remove_all_tags(html_text):
    '''
    去除文本中所有HTML标签
    参数：
    html_text:包含HTML标签的文本
    '''
    return re.sub(r'<[^>]+>', '', html_text)

def remove_urls_clean(text):
    ''''
    删除URL并清除多余空格
    '''
    #删除url
    no_urls=re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w.\-?=%&:#@$,;*!]*', '', text)
    #清理连续空格和空行
    return re.sub(r'\s+','',no_urls).strip()

def clean_string(text):
    text=remove_urls_clean(text)
    text=remove_all_tags(text)
    pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4bdf\U00020000-\U0002a6dfa-zA-z0-9]')
    return ''.join(pattern.findall(text))