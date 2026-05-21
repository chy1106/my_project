import re

from flask import Flask, request, session, redirect

from view.page import page
from view.user import user

app = Flask(__name__)
app.secret_key='admin'

#注册蓝图
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

@app.before_request
def before_request():
    """
    鉴权
    :return:
    """
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    if request.path == '/user/login':
        return
    if request.path == '/user/register':
        return
    user = session.get('user')
    if user:
        return None
    return redirect('/user/login')

if __name__ == '__main__':
    app.run()
