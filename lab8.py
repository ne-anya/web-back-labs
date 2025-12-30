from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, logout_user, current_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form or not password_form:
        return render_template('lab8/register.html', 
                               error='Логин и пароль не должны быть пустыми')
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                               error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=False)
    
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember')
    
    if not login_form or not password_form:
        return render_template('lab8/login.html', 
                               error='Логин и пароль не должны быть пустыми')
    
    user = users.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        remember = True if remember_me == 'on' else False
        login_user(user, remember=remember)
        return redirect('/lab8/')
    
    return render_template('lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_title = request.form.get('article_title')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_title:
        return render_template('lab8/create.html', 
                               error='Заголовок и текст статьи обязательны для заполнения')
    
    try:
        new_article = articles(
        title=title,
        article_title=article_title,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0,
        login_id=current_user.id
    )
        
        db.session.add(new_article)
        db.session.commit()
        
        flash('Статья успешно создана!', 'success')
        return redirect('/lab8/articles/')
        
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/create.html', 
                               error=f'Ошибка при создании статьи: {str(e)}')
    

@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        flash('Статья не найдена или у вас нет прав на ее редактирование', 'error')
        return redirect('/lab8/articles/')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_title = request.form.get('article_title')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_title:
        return render_template('lab8/edit.html', article=article,
                               error='Заголовок и текст статьи обязательны для заполнения')
    
    try:
        article.title = title
        article.article_title = article_title
        article.is_public = is_public
        article.is_favorite = is_favorite
        article.likes = article.likes
        
        db.session.commit()
        
        flash('Статья успешно обновлена!', 'success')
        return redirect('/lab8/articles/')
        
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/edit.html', article=article,
                               error=f'Ошибка при обновлении статьи: {str(e)}')
    

@lab8.route('/lab8/delete/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        flash('Статья не найдена или у вас нет прав на ее удаление', 'error')
        return redirect('/lab8/articles/')
    
    if request.method == 'GET':
        return render_template('lab8/delete.html', article=article)
    
    try:
        db.session.delete(article)
        db.session.commit()
        
        flash(f'Статья "{article.title}" успешно удалена!', 'success')
        return redirect('/lab8/articles/')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении статьи: {str(e)}', 'error')
        return redirect('/lab8/articles/')