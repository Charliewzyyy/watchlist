from flask import render_template

from watchlist import app

### 400 错误处理函数
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400

### 404 错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

### 500 错误处理函数
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500