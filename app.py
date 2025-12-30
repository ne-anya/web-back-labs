from flask import Flask, url_for, request
from db import db

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
# from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

import datetime
import os
from os import path


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'anna_votchinnikova_orm'
    db_user = 'anna_votchinnikova_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
    
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "anna_votchinnikova_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
# app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


@app.route("/")
@app.route("/index")
def index():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
            <hr>
        </header>
        <main>
            <li>
                <ol><a href="/lab1">Первая лабораторная</a></ol>
                <ol><a href="/lab2">Вторая лабораторная</a></ol>
                <ol><a href="/lab3/">Третья лабораторная</a></ol>
                <ol><a href="/lab4/">Четвертая лаборатораная</a></ol>
                <ol><a href="/lab5/">Пятая лабораторная</a></ol>
                <ol><a href="/lab6/">Шестая лабораторная</a></ol>
                <ol><a href="/lab7/">Седьмая лабораторная</a></ol>
                <ol><a href="/lab8/">Восьмая лабораторная</a></ol>
            </li>
        </main>
        <footer>
            <hr>
            Вотчинникова Анна, ФБИ-33, 3 курс, 2025 год
        </footer>
    </body>
</html>
"""


@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="lab1/404.webp")
    style = url_for("static", filename="lab1/lab1.css")
    client_ip = request.remote_addr
    access_time = datetime.datetime.today()
    requested_url = request.url
    return '''
<!doctype html>
<link rel="stylesheet" href="''' + style + '''">
<html>
    <body>
        <h1>Не найдено</h1>
        <div>Неправильно набран адрес или 
        такой страницы больше не существует</div>
        <img src="''' + path +'''">
        <div class="info-box">
            <p><strong>Ваш IP-адрес:</strong>''' + client_ip + '''</p>
            <p><strong>Дата и время доступа:</strong> ''' + access_time.strftime('%Y-%m-%d %H:%M:%S') + '''</p>
            <p><strong>Запрошенный адрес:</strong> ''' + requested_url + '''</p>
        </div>
    </body>
</html>
''', 404


@app.errorhandler(500)
def error(err):
    style = url_for("static", filename="lab1/lab1.css")
    return '''
<!doctype html>
<link rel="stylesheet" href="''' + style + '''">
<html>
    <body>
        <h1>500</h1>
        <div>Внутренняя ошибка сервера</div>
    </body>
</html>
''', 500


@app.route("/server_error")
def server_error():
    result = 2 / 0
    return "Этот код никогда не выполнится"


