from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
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


@lab2.route('/lab2/flowers')
def flowers():
    return render_template('lab2/flowers.html', flowers=flower_list)


@lab2.route('/lab2/add_flower')
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
    
    flower_list.lab2end({"name": name, "price": price_int})
    
    return redirect(url_for('flowers'))


@lab2.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    
    deleted_flower = flower_list.pop(flower_id)
    
    return redirect(url_for('flowers'))


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('flowers'))


@lab2.route('/lab2/flower/<int:flower_id>')
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


@lab2.route('/lab2/example')
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
    return render_template('lab2/example.html', 
                           name=name, lab=lab, group=group, 
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
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


@lab2.route('/lab2/books')
def books():
    total_pages = sum(book['pages'] for book in books_list)
    
    return render_template('lab2/books.html', 
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


@lab2.route('/lab2/cats')
def cats_gallery():
    return render_template('lab2/cats.html', cats=cats_list)