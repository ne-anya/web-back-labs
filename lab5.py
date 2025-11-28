from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'anna_votchinnikova_knowledge_base',
            user = 'anna_votchinnikova_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                            error = "Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль не верны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'true'  
    is_favorite = request.form.get('is_favorite') == 'true'

    if not title or not title.strip():
        return render_template('lab5/create_article.html', 
                             error='Название статьи не может быть пустым')
    
    if not article_text or not article_text.strip():
        return render_template('lab5/create_article.html', 
                             error='Текст статьи не может быть пустым')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(login_id, title, article_text, is_public, is_favorite, likes) \
                VALUES(%s, %s, %s, %s, %s, %s);", (login_id, title, article_text, is_public, is_favorite, likes))
    else:
        cur.execute("INSERT INTO articles(login_id, title, article_text, is_public, is_favorite, likes) \
                VALUES(?, ?, ?, ?, ?, ?);", (login_id, title, article_text, is_public, is_favorite, likes))
    
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], message="Пользователь не найден")
    
    login_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT * FROM articles 
            WHERE login_id=%s 
            ORDER BY is_favorite DESC, id DESC;
        """, (login_id,))
    else:
        cur.execute("""
            SELECT * FROM articles 
            WHERE login_id=? 
            ORDER BY is_favorite DESC, id DESC;
        """, (login_id,))

    articles = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('/lab5/articles.html', articles=articles)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)

    return redirect('/lab5')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], 
                             message="Статья не найдена")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], 
                             message="Пользователь не найден")

    if article['login_id'] != user['id']:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], 
                             message="У вас нет прав для редактирования этой статьи")

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('/lab5/edit_article.html', 
                             article=article, 
                             article_id=article_id)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'true'
    is_favorite = request.form.get('is_favorite') == 'true'

    if not title or not title.strip():
        db_close(conn, cur)
        return render_template('/lab5/edit_article.html', 
                             article=article,
                             article_id=article_id,
                             error='Название статьи не может быть пустым')
    
    if not article_text or not article_text.strip():
        db_close(conn, cur)
        return render_template('/lab5/edit_article.html', 
                             article=article,
                             article_id=article_id,
                             error='Текст статьи не может быть пустым')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE articles 
            SET title=%s, article_text=%s, is_public=%s, is_favorite=%s 
            WHERE id=%s;
        """, (title.strip(), article_text.strip(), is_public, is_favorite, article_id))
    else:
        cur.execute("""
            UPDATE articles 
            SET title=?, article_text=?, is_public=?, is_favorite=? 
            WHERE id=?;
        """, (title.strip(), article_text.strip(), is_public, is_favorite, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], 
                             message="Статья не найдена")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], 
                             message="Пользователь не найден")

    if article['login_id'] != user['id']:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], 
                             message="У вас нет прав для удаления этой статьи")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)

    return redirect('/lab5/list?message=Статья успешно удалена')


@lab5.route('/lab5/users')
def all_users():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('/lab5/all_users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('/lab5/profile.html', user=user)

    new_real_name = request.form.get('real_name')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()

    errors = []

    if new_password:
        if not current_password:
            errors.append('Введите текущий пароль для смены пароля')
        elif not check_password_hash(user['password'], current_password):
            errors.append('Текущий пароль неверен')
        elif new_password != confirm_password:
            errors.append('Новый пароль и подтверждение не совпадают')
        elif len(new_password) < 3:
            errors.append('Новый пароль должен быть не менее 3 символов')

    if errors:
        db_close(conn, cur)
        return render_template('/lab5/profile.html', user=user, errors=errors)

    if new_password:
        new_password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s, password=%s WHERE login=%s;", 
                       (new_real_name, new_password_hash, login))
        else:
            cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;", 
                       (new_real_name, new_password_hash, login))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", 
                       (new_real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?;", 
                       (new_real_name, login))

    db_close(conn, cur)
    
    return redirect('/lab5/profile?message=Данные успешно обновлены')


@lab5.route('/lab5/favorite/<int:article_id>')
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.id=%s AND u.login=%s;
        """, (article_id, login))
    else:
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.id=? AND u.login=?;
        """, (article_id, login))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list?error=Статья не найдена')

    new_favorite_status = not article['is_favorite']
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", 
                   (new_favorite_status, article_id))
    else:
        cur.execute("UPDATE articles SET is_favorite=? WHERE id=?;", 
                   (new_favorite_status, article_id))

    db_close(conn, cur)
    
    action = "добавлена в избранное" if new_favorite_status else "убрана из избранного"
    return redirect(f'/lab5/list?message=Статья {action}')


@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.*, u.login, u.real_name 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = true 
            ORDER BY a.likes DESC, a.id DESC;
        """)
    else:
        cur.execute("""
            SELECT a.*, u.login, u.real_name 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = 1 
            ORDER BY a.likes DESC, a.id DESC;
        """)
    
    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('/lab5/public_articles.html', 
                         articles=articles, 
                         login=session.get('login'))


@lab5.route('/lab5/like/<int:article_id>')
def like_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND is_public=true;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND is_public=1;", (article_id,))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return redirect('/lab5/public?error=Статья не найдена или не публичная')

    new_likes = (article['likes'] or 0) + 1
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET likes=%s WHERE id=%s;", (new_likes, article_id))
    else:
        cur.execute("UPDATE articles SET likes=? WHERE id=?;", (new_likes, article_id))

    db_close(conn, cur)
    
    return redirect('/lab5/public?message=Лайк добавлен')