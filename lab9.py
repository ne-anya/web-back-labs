from flask import Blueprint, render_template, session, jsonify, request
from flask_login import current_user
from db import db
from db.models import gifts
import random
import uuid

lab9 = Blueprint('lab9', __name__)

# 10 поздравлений (без картинок подарков!)
congratulations = [
    "С Новым годом! Желаю счастья и удачи!",
    "Пусть новый год принесет много радости!",
    "Желаю исполнения всех желаний!",
    "Пусть ангел-хранитель оберегает вас!",
    "Желаю финансового благополучия!",
    "Пусть в доме всегда будет тепло!",
    "Желаю крепкого здоровья!",
    "Пусть год будет полон сюрпризов!",
    "Желаю любви и семейного счастья!",
    "Желаю интересных путешествий!"
]

@lab9.route('/lab9/')
def index():
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())
    
    sid = session['sid']
    
    opened = gifts.query.filter_by(session_id=sid).all()
    opened_ids = [g.gift_number for g in opened]
    opened_count = len(opened_ids)
    unopened_count = 10 - opened_count
    
    # Позиции картинок
    if 'positions' not in session:
        positions = []
        for i in range(10):
            positions.append({
                'top': f"{random.randint(10, 70)}%",
                'left': f"{random.randint(5, 85)}%"
            })
        session['positions'] = positions
    else:
        positions = session['positions']
    
    return render_template('lab9/index.html',
                         positions=positions,
                         opened=opened_ids,
                         opened_count=opened_count,
                         unopened_count=unopened_count)

@lab9.route('/lab9/open', methods=['POST'])
def open_gift():
    try:
        data = request.get_json()
        gift_id = int(data['id'])
        
        sid = session.get('sid')
        
        if gifts.query.filter_by(session_id=sid, gift_number=gift_id).first():
            return jsonify({"success": False, "message": "Этот подарок уже открыт!"})
        
        opened_count = gifts.query.filter_by(session_id=sid).count()
        if opened_count >= 3:
            return jsonify({"success": False, "message": "Вы уже открыли 3 подарка! Больше нельзя."})
        
        gift = gifts(
            session_id=sid,
            gift_number=gift_id,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(gift)
        db.session.commit()
        
        new_opened_count = opened_count + 1
        new_unopened_count = 10 - new_opened_count
        
        return jsonify({
            "success": True,
            "congratulation": congratulations[gift_id - 1],
            "opened_count": new_opened_count,
            "unopened_count": new_unopened_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Ошибка: {str(e)}"})