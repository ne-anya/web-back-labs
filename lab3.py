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