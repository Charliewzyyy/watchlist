import click

from watchlist import app, db
from watchlist.models import User, Movie

### 自定义命令 initdb
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


### 创建自定义命令 forge
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Charliewzyyy'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


### 生成管理员账户
@app.cli.command()  # 使用 click.option() 装饰器设置的两个选项分别用来接受输入用户名和密码
@click.option('--username', prompt=True, help='The username used to login.')
# hide_input=True:在命令行中输入密码时不会显示输入内容，confirmation_prompt=True:用户需要确认密码
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:  # 若数据库中已存在用户，表示管理员用户已经创建过，接下来会更新用户名和密码
        click.echo('Updating user...')  # 在命令行输出消息
        user.username = username
        user.set_password(password)  # 设置密码 调用User类的set_password函数
    else:  # 输入用户名和密码后，即可创建管理员账户
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')
