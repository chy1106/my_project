# _*_coding : utf-8 _*_
# @Time : 2026/3/3 11:03
# @File : UserModel
# @Project : weiboProject

class User:
    id=None
    username=None
    password=None
    createtime=None

    def __init__(self,username,password):
        self.username=username
        self.password=password