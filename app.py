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
                <ol><a href="/lab2">Вторая лабораторная</a></ol>
            </li>
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

flower_list = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка", "price": 330},
    {"name": "георгин", "price": 300},
    {"name": "гладиолус", "price": 310}
]

@app.route('/lab2/flowers')
def all_flowers():
    return render_template('flowers.html', flowers=flower_list)

@app.route('/lab2/add_flower')
def add_flower():
    name = request.args.get('name', '').strip()
    price = request.args.get('price', '').strip()
    
    if not name or not price:
        abort(400, "Вы не задали имя цветка или цену")
    
    try:
        price_int = int(price)
        if price_int <= 0:
            abort(400, "Цена должна быть положительным числом")
    except ValueError:
        abort(400, "Цена должна быть числом")
    
    flower_list.append({"name": name, "price": price_int})
    
    return redirect(url_for('all_flowers'))

@app.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    
    deleted_flower = flower_list.pop(flower_id)
    
    return redirect(url_for('all_flowers'))

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('all_flowers'))

@app.route('/lab2/flower/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id]
        return f'''
        <!doctype html>
        <html>
            <head>
                <title>Цветок #{flower_id}</title>
                <link rel="stylesheet" href="{{ url_for('static', filename='main.css')}}">
            </head>
            <body>
                <header>
                    <nav class="main-nav">
                        <a href="/" class="nav-home">Главная</a>
                        <span class="nav-title">WEB-программирование, часть 2. Цветок</span>
                    </nav>
                </header>
                <main style="padding: 2rem;">
                    <h1>Информация о цветке</h1>
                    <p><strong>Название:</strong> {flower['name']}</p>
                    <p><strong>Цена:</strong> {flower['price']} руб</p>
                    <p><strong>ID:</strong> {flower_id}</p>
                    <a href="/lab2/flowers">← Вернуться к списку всех цветов</a>
                </main>
                <footer>
                    &copy; Анна Вотчинникова, ФБИ-33, 3 курс, 2025
                </footer>
            </body>
        </html>
        '''

@app.route('/lab2/example')
def example():
    name = 'Анна Вотчинникова'
    lab = 2
    group = 'ФБИ-33'
    course = 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120}, 
        {'name': 'апельсины', 'price': 80}, 
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321} 
    ]
    return render_template('example.html', 
                           name=name, lab=lab, group=group, 
                           course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
<!doctype html>
<html>
    <head>
        <title>Калькулятор</title>
    </head>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {a + b}</p>
        <p>{a} - {b} = {a - b}</p>
        <p>{a} × {b} = {a * b}</p>
        <p>{a} / {b} = {a / b if b != 0 else '∞ (деление на ноль)'}</p>
        <p>{a}<sup>{b}</sup> = {a ** b}</p>
    </body>
</html>
'''

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

books_list = [
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
    {"author": "Антон Чехов", "title": "Рассказы", "genre": "Рассказы", "pages": 320},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Роман", "pages": 480},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 240},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Поэма", "pages": 352},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 288},
    {"author": "Александр Солженицын", "title": "Один день Ивана Денисовича", "genre": "Повесть", "pages": 142},
    {"author": "Михаил Лермонтов", "title": "Герой нашего времени", "genre": "Роман", "pages": 224},
    {"author": "Иван Бунин", "title": "Тёмные аллеи", "genre": "Рассказы", "pages": 196},
    {"author": "Владимир Набоков", "title": "Лолита", "genre": "Роман", "pages": 336},
    {"author": "Борис Пастернак", "title": "Доктор Живаго", "genre": "Роман", "pages": 592}
]

@app.route('/lab2/books')
def books():
    total_pages = sum(book['pages'] for book in books_list)
    
    return render_template('books.html', 
                         books=books_list, 
                         total_pages=total_pages)

cats_list = [
    {
        "name": "Барсик",
        "breed": "Британская короткошёрстная",
        "age": "3 года",
        "color": "Серый",
        "image": "barsik.jpg"
    },
    {
        "name": "Мурка",
        "breed": "Сиамская",
        "age": "2 года",
        "color": "Крем-пойнт",
        "image": "murka.jpg"
    },
    {
        "name": "Васька",
        "breed": "Дворовый",
        "age": "4 года",
        "color": "Рыжий",
        "image": "vaska.jpg"
    },
    {
        "name": "Снежка",
        "breed": "Турецкая ангора",
        "age": "1.5 года",
        "color": "Белый",
        "image": "snezhka.jpg"
    },
    {
        "name": "Гарфилд",
        "breed": "Экзотическая короткошёрстная",
        "age": "5 лет",
        "color": "Рыже-белый",
        "image": "garfield.jpg"
    },
    {
        "name": "Луна",
        "breed": "Шотландская вислоухая",
        "age": "2 года",
        "color": "Серебристый табби",
        "image": "luna.jpg"
    },
    {
        "name": "Симба",
        "breed": "Мейн-кун",
        "age": "4 года",
        "color": "Красный мраморный",
        "image": "simba.jpg"
    },
    {
        "name": "Багира",
        "breed": "Бомбейская",
        "age": "3 года",
        "color": "Чёрный",
        "image": "bagira.jpg"
    },
    {
        "name": "Рыжик",
        "breed": "Норвежская лесная",
        "age": "6 лет",
        "color": "Рыжий с белым",
        "image": "ryzhik.jpg"
    },
    {
        "name": "Зося",
        "breed": "Сфинкс",
        "age": "2 года",
        "color": "Розовый",
        "image": "zosya.jpg"
    },
    {
        "name": "Тигра",
        "breed": "Бенгальская",
        "age": "3 года",
        "color": "Леопардовый",
        "image": "tigra.jpg"
    },
    {
        "name": "Персик",
        "breed": "Рэгдолл",
        "age": "2.5 года",
        "color": "Сил-пойнт",
        "image": "persik.jpg"
    },
    {
        "name": "Дымка",
        "breed": "Русская голубая",
        "age": "4 года",
        "color": "Голубой",
        "image": "dymka.jpg"
    },
    {
        "name": "Кексик",
        "breed": "Скоттиш-страйт",
        "age": "1 год",
        "color": "Черепаховый",
        "image": "keksik.jpg"
    },
    {
        "name": "Ночка",
        "breed": "Ориентальная",
        "age": "2 года",
        "color": "Эбони",
        "image": "nochka.jpg"
    },
    {
        "name": "Маркиз",
        "breed": "Персидская",
        "age": "5 лет",
        "color": "Дымчатый",
        "image": "markiz.jpg"
    },
    {
        "name": "Ириска",
        "breed": "Абиссинская",
        "age": "3 года",
        "color": "Дикий",
        "image": "iriska.jpg"
    },
    {
        "name": "Пушок",
        "breed": "Сибирская",
        "age": "4 года",
        "color": "Чёрный дым",
        "image": "pushok.jpg"
    },
    {
        "name": "Сема",
        "breed": "Корниш-рекс",
        "age": "2 года",
        "color": "Белый",
        "image": "sema.jpg"
    },
    {
        "name": "Бусинка",
        "breed": "Девон-рекс",
        "age": "1.5 года",
        "color": "Голубой",
        "image": "businka.jpg"
    }
]

@app.route('/lab2/cats')
def cats_gallery():
    return render_template('cats.html', cats=cats_list)