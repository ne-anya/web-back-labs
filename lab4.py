from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods= ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/summ-form')
def summ_form():
    return render_template('lab4/summ-form.html')


@lab4.route('/lab4/summ', methods= ['POST'])
def summ():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/summ.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods= ['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods= ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')


@lab4.route('/lab4/exp', methods= ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/exp.html', error='Оба поля должны быть заполнены')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/exp.html', error='Оба поля равны нулю')
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)

tree_count = 0


@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'maria', 'password': '555', 'name': 'Мария Иванова', 'gender': 'female'},
    {'login': 'anna', 'password': '654', 'name': 'Анна Вотчинникова', 'gender': 'female'},
    {'login': 'liza', 'password': '987', 'name': 'Елизавета Иванова', 'gender': 'female'},
]


@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_data = next((user for user in users if user['login'] == session['login']), None)
            name = user_data['name'] if user_data else session['login']
            if user_data:
                name = user_data['name']
            else:
                name = session['login']
                session.pop('login', None)
                authorized = False
            return render_template("lab4/login.html", authorized=authorized, name=name)
        else:
            authorized = False
            return render_template("lab4/login.html", authorized=authorized)
    
    login = request.form.get('login')
    password = request.form.get('password')
    previous_login = login

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, previous_login=previous_login)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, previous_login=previous_login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, previous_login=previous_login)


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    
    if not login:
        return render_template('lab4/register.html', error='Не введён логин', login=login, name=name)
    
    if not name:
        return render_template('lab4/register.html', error='Не введено имя', login=login, name=name)
    
    if not password:
        return render_template('lab4/register.html', error='Не введён пароль', login=login, name=name)
    
    if password != password_confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают', login=login, name=name)
    
    for user in users:
        if user['login'] == login:
            return render_template('lab4/register.html', error='Логин уже занят', login=login, name=name)
    
    new_user = {
        'login': login,
        'password': password,
        'name': name
    }
    users.append(new_user)
    
    session['login'] = login
    return redirect('/lab4/login')

@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    return render_template('lab4/users.html', users=users, current_user_login=current_user_login)

@lab4.route('/lab4/users/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    
    global users
    users = [user for user in users if user['login'] != current_user_login]
    
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/users/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    current_user = next((user for user in users if user['login'] == current_user_login), None)
    
    if not current_user:
        session.pop('login', None)
        return redirect('/lab4/login')
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', user=current_user)
    
    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    
    if not new_login:
        return render_template('lab4/edit_user.html', user=current_user, error='Не введён логин')
    
    if not new_name:
        return render_template('lab4/edit_user.html', user=current_user, error='Не введено имя')
    
    for user in users:
        if user['login'] == new_login and user['login'] != current_user_login:
            return render_template('lab4/edit_user.html', user=current_user, error='Логин уже занят')
    
    current_user['login'] = new_login
    current_user['name'] = new_name
    
    if new_password:
        if new_password != password_confirm:
            return render_template('lab4/edit_user.html', user=current_user, error='Пароли не совпадают')
        current_user['password'] = new_password
    
    if new_login != current_user_login:
        session['login'] = new_login
    
    return redirect('/lab4/users')


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge')
def fridge_form():
    return render_template('lab4/fridge.html')

@lab4.route('/lab4/fridge', methods=['POST'])
def fridge():
    temperature_str = request.form.get('temperature')
    
    if not temperature_str:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temperature = int(temperature_str)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: температура должна быть числом')
    
    if temperature < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temperature > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temperature <= -9:
        snowflakes = 3
        message = f'Установлена температура: {temperature}°C'
    elif -8 <= temperature <= -5:
        snowflakes = 2
        message = f'Установлена температура: {temperature}°C'
    elif -4 <= temperature <= -1:
        snowflakes = 1
        message = f'Установлена температура: {temperature}°C'
    else:
        snowflakes = 0
        message = f'Установлена температура: {temperature}°C'
    
    return render_template('lab4/fridge.html', 
                         message=message, 
                         snowflakes=snowflakes, 
                         temperature=temperature)


@lab4.route('/lab4/grain_order')
def grain_order_form():
    return render_template('lab4/grain_order.html')

@lab4.route('/lab4/grain_order', methods=['POST'])
def grain_order():
    grain_type = request.form.get('grain_type')
    weight_str = request.form.get('weight')
    
    prices = {
        'barley': 12000,   
        'oats': 8500,      
        'wheat': 9000,    
        'rye': 15000       
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if not weight_str:
        return render_template('lab4/grain_order.html', 
                             error='Ошибка: не указан вес заказа')
    
    try:
        weight = float(weight_str)
    except ValueError:
        return render_template('lab4/grain_order.html', 
                             error='Ошибка: вес должен быть числом')
    
    if weight <= 0:
        return render_template('lab4/grain_order.html', 
                             error='Ошибка: вес должен быть больше 0')
    
    if weight > 100:
        return render_template('lab4/grain_order.html', 
                             error='Извините, такого объёма сейчас нет в наличии')
    
    if not grain_type or grain_type not in prices:
        return render_template('lab4/grain_order.html', 
                             error='Ошибка: не выбрано зерно')
    
    price_per_ton = prices[grain_type]
    total_cost = weight * price_per_ton
    discount = 0
    discount_applied = False
    
    if weight > 10:
        discount = total_cost * 0.10
        total_cost -= discount
        discount_applied = True
    
    grain_name = grain_names[grain_type]
    
    return render_template('lab4/grain_order.html',
                         success=True,
                         grain_name=grain_name,
                         weight=weight,
                         total_cost=total_cost,
                         discount_applied=discount_applied,
                         discount=discount)