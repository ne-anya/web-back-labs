from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    if not name:
        name = "Аноним"
    if not age:
        age = "неизвестно"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar'):
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color=request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')
    if color or bg_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_style = request.cookies.get('font_style')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_style=font_style))
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket.html')

@lab3.route('/lab3/ticket_result')
def ticket_result():
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    errors = []
    if not fio:
        errors.append("ФИО пассажира обязательно")
    if not shelf:
        errors.append("Выберите полку")
    if not age:
        errors.append("Возраст обязателен")
    elif not age.isdigit() or int(age) < 1 or int(age) > 120:
        errors.append("Возраст должен быть от 1 до 120 лет")
    if not departure:
        errors.append("Пункт выезда обязателен")
    if not destination:
        errors.append("Пункт назначения обязателен")
    if not date:
        errors.append("Дата поездки обязательна")
    
    if errors:
        return render_template('lab3/ticket.html', errors=errors)
    
    if int(age) < 18:
        ticket_type = "Детский билет"
        base_price = 700
    else:
        ticket_type = "Взрослый билет"
        base_price = 1000
    
    additions = []
    if shelf in ['lower', 'lower-side']:
        base_price += 100
        additions.append("+100 руб. (нижняя полка)")
    
    if linen == 'on':
        base_price += 75
        additions.append("+75 руб. (бельё)")
    
    if baggage == 'on':
        base_price += 250
        additions.append("+250 руб. (багаж)")
    
    if insurance == 'on':
        base_price += 150
        additions.append("+150 руб. (страховка)")
    
    return render_template('lab3/ticket_result.html',
                         fio=fio,
                         shelf=shelf,
                         linen=linen,
                         baggage=baggage,
                         age=age,
                         departure=departure,
                         destination=destination,
                         date=date,
                         insurance=insurance,
                         ticket_type=ticket_type,
                         base_price=base_price,
                         additions=additions)


@lab3.route('/lab3/search')
def search():
    # Список товаров (смартфоны)
    products = [
        {'name': 'iPhone 15', 'price': 89990, 'brand': 'Apple', 'color': 'черный', 'storage': '128GB'},
        {'name': 'Samsung Galaxy S24', 'price': 79990, 'brand': 'Samsung', 'color': 'белый', 'storage': '256GB'},
        {'name': 'Xiaomi Redmi Note 13', 'price': 24990, 'brand': 'Xiaomi', 'color': 'синий', 'storage': '128GB'},
        {'name': 'Google Pixel 8', 'price': 64990, 'brand': 'Google', 'color': 'серый', 'storage': '128GB'},
        {'name': 'OnePlus 12', 'price': 59990, 'brand': 'OnePlus', 'color': 'зеленый', 'storage': '256GB'},
        {'name': 'iPhone 14', 'price': 69990, 'brand': 'Apple', 'color': 'красный', 'storage': '128GB'},
        {'name': 'Samsung Galaxy A54', 'price': 32990, 'brand': 'Samsung', 'color': 'фиолетовый', 'storage': '128GB'},
        {'name': 'Xiaomi 13T', 'price': 44990, 'brand': 'Xiaomi', 'color': 'черный', 'storage': '256GB'},
        {'name': 'Realme 11 Pro', 'price': 27990, 'brand': 'Realme', 'color': 'золотой', 'storage': '128GB'},
        {'name': 'Nothing Phone 2', 'price': 49990, 'brand': 'Nothing', 'color': 'белый', 'storage': '256GB'},
        {'name': 'iPhone 13', 'price': 59990, 'brand': 'Apple', 'color': 'розовый', 'storage': '128GB'},
        {'name': 'Samsung Galaxy S23', 'price': 64990, 'brand': 'Samsung', 'color': 'кремовый', 'storage': '256GB'},
        {'name': 'Xiaomi Poco X6', 'price': 21990, 'brand': 'Xiaomi', 'color': 'желтый', 'storage': '128GB'},
        {'name': 'Google Pixel 7a', 'price': 39990, 'brand': 'Google', 'color': 'коралловый', 'storage': '128GB'},
        {'name': 'OnePlus Nord 3', 'price': 34990, 'brand': 'OnePlus', 'color': 'серый', 'storage': '256GB'},
        {'name': 'iPhone SE', 'price': 44990, 'brand': 'Apple', 'color': 'белый', 'storage': '64GB'},
        {'name': 'Samsung Galaxy Z Flip5', 'price': 99990, 'brand': 'Samsung', 'color': 'фиолетовый', 'storage': '256GB'},
        {'name': 'Xiaomi Redmi 12', 'price': 15990, 'brand': 'Xiaomi', 'color': 'серебристый', 'storage': '128GB'},
        {'name': 'Motorola Edge 40', 'price': 37990, 'brand': 'Motorola', 'color': 'черный', 'storage': '256GB'},
        {'name': 'Honor 90', 'price': 29990, 'brand': 'Honor', 'color': 'изумрудный', 'storage': '256GB'}
    ]
    
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    min_price_form = request.args.get('min_price')
    max_price_form = request.args.get('max_price')
    reset = request.args.get('reset')
    
    if reset:
        resp = make_response(render_template('lab3/search.html', 
                                           products=products, 
                                           min_price='', 
                                           max_price='',
                                           count=len(products)))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    if min_price_form is not None or max_price_form is not None:
        min_price = min_price_form if min_price_form != '' else None
        max_price = max_price_form if max_price_form != '' else None
    else:
        min_price = min_price_cookie
        max_price = max_price_cookie
    
    if min_price and max_price and float(min_price) > float(max_price):
        min_price, max_price = max_price, min_price
    
    filtered_products = []
    for product in products:
        price = product['price']
        if min_price and max_price:
            if float(min_price) <= price <= float(max_price):
                filtered_products.append(product)
        elif min_price:
            if price >= float(min_price):
                filtered_products.append(product)
        elif max_price:
            if price <= float(max_price):
                filtered_products.append(product)
        else:
            filtered_products.append(product)
    
    resp = make_response(render_template('lab3/search.html', 
                                       products=filtered_products, 
                                       min_price=min_price or '',
                                       max_price=max_price or '',
                                       count=len(filtered_products)))
    
    if min_price_form is not None or max_price_form is not None:
        if min_price:
            resp.set_cookie('min_price', min_price, max_age=60*60*24*30)
        else:
            resp.delete_cookie('min_price')
        
        if max_price:
            resp.set_cookie('max_price', max_price, max_age=60*60*24*30)
        else:
            resp.delete_cookie('max_price')
    
    return resp