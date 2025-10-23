from flask import Blueprint, url_for, request, redirect
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")
def lab():
    return """
<!doctype html>
<html>
    <head>
        <title>Лабораторная работа 1</title>
    </head>
    <body>
        <h1>Лабораторная работа 1</h1>
        <div>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.
        </div>
        <h2>Список роутов</h2>
        <li>
            <ol><a href="/lab1/web">Web</a></ol>
            <ol><a href="/lab1/author">Author</a></ol>
            <ol><a href="/lab1/image">Image</a></ol>
            <ol><a href="/lab1/counter">Counter</a></ol>
            <ol><a href="/bad_request">Bad request</a></ol>
            <ol><a href="/unauthorized">Unautorized</a></ol>
            <ol><a href="/payment_required">Payment Required</a></ol>
            <ol><a href="/forbidden">Forbidden</a></ol>
            <ol><a href="/method_not_allowed">Method Not Allowed</a></ol>
            <ol><a href="/teapot">Teapot</a></ol>
            <ol><a href="/404">404</a></ol>
            <ol><a href="/server_error">500</a></ol>
        <a href="/index">На главную страницу</a>
    </body>
</html>
"""


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html> 
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">Автор</a>
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/plain; charset=utf-8" 
        }


@lab1.route("/lab1/author")
def author():
    name = "Вотчинникова Анна Андреевна"
    group = "ФБИ-33"
    faculty = "ФБ"
    
    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    style = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<link rel="stylesheet" href="''' + style + '''">
<html>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path +'''">
    </body>
</html>
''', 200, {
    'Content-Language': 'ru-Ru',
    'X-Server-Location': 'Novosibirsk',
    'X-Student-Name': 'Anna Votchinnikova'
}


count = 0


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <a href="/lab1/clear_counter">Отчистить счетчик</a>
    </body>
<html>
'''


@lab1.route("/lab1/clear_counter")
def clear_counter():
    global count
    count=0
    return redirect("/lab1/counter")


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201