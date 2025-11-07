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


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')