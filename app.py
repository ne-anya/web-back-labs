from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

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
        </main>
        <footer>
            <hr>
            Вотчинникова Анна, ФБИ-33, 3 курс, 2025 год
        </footer>
    </body>
</html>
"""
@app.route("/lab1")
def lab1():
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

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route('/lab1/image')
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

@app.route('/lab1/counter')
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

@app.route("/lab1/clear_counter")
def clear_counter():
    global count
    count=0
    return redirect("/lab1/counter")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
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

@app.route("/bad_request")
def bad_reqeust():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Bad Request</h1>
        <div>Cервер не может понять или обработать запрос 
        из-за синтаксической ошибки</div>
    </body>
</html>
''', 400

@app.route("/unauthorized")
def unauthorized():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Unauthorized</h1>
        <div>Неавторизованный запрос</div>
    </body>
</html>
''', 401

@app.route("/payment_required")
def payment_required():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Payment Required</h1>
        <div>Необходима оплата</div>
    </body>
</html>
''', 402

@app.route("/forbidden")
def forbidden():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Forbidden</h1>
        <div>Доступ запрещен</div>
    </body>
</html>
''', 403

@app.route("/method_not_allowed")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Method Not Allowed</h1>
        <div>Метод не поддерживается</div>
    </body>
</html>
''', 405

@app.route("/teapot")
def teapot():
    return '''
<!doctype html>
<html>
    <body>
        <h1>I’m a teapot</h1>
        <div>Сервер отказывается варить кофе, 
        потому что это чайник</div>
    </body>
</html>
''', 418

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="404.webp")
    style = url_for("static", filename="lab1.css")
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
    style = url_for("static", filename="lab1.css")
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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flower/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<doctype html!>
<html>
    <body>
        <h1>Добавлен цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html
'''

@app.route('/lab2/example')
def example():
    return render_template('example.html')