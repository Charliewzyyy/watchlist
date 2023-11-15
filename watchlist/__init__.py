import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# from watchlist import app, db
# from watchlist.models import User, Movie


### 数据库配置
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
# 设置签名所需的密钥
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# SQLAlchemy 数据库连接地址：
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例app
login_manager = LoginManager(app)

login_manager.login_view = 'login'  # 重定向操作 把 login_manager.login_view 的值设为程序的登录视图端点（函数名）


### 初始化 Flask-Login
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


### 模板上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}
    # 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。
    # 后面我们创建的任意一个模板，都可以在模板中直接使用 user 变量。


from watchlist import views, errors, commands
