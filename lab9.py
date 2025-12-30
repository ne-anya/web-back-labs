from flask import Blueprint, render_template, session, jsonify, request
from flask_login import current_user, login_required
import random
import uuid

lab9 = Blueprint('lab9', __name__)

# 10 уникальных поздравлений
CONGRATULATIONS = [
    "🎄 С Новым годом! Желаю счастья, здоровья и удачи в новом году!",
    "🎅 Пусть новый год принесет много радости, улыбок и тепла!",
    "🌟 Желаю исполнения всех желаний и заветных мечтаний!",
    "❄️ Пусть ангел-хранитель оберегает вас весь год!",
    "💰 Желаю финансового благополучия и карьерного роста!",
    "🏠 Пусть в вашем доме всегда будет уют, тепло и гармония!",
    "💪 Желаю крепкого здоровья, бодрости духа и энергии!",
    "🎁 Пусть новый год будет полон приятных сюрпризов и подарков!",
    "❤️ Желаю любви, взаимопонимания и семейного счастья!",
    "✈️ Желаю интересных путешествий, новых открытий и впечатлений!"
]

# 10 картинок подарков
GIFT_IMAGES = [
    "gift1.jpg", "gift2.jpg", "gift3.jpg", "gift4.jpg", "gift5.jpg",
    "gift6.jpg", "gift7.jpg", "gift8.jpg", "gift9.jpg", "gift10.jpg"
]

# Подарки только для авторизованных (номера 8, 9, 10)
AUTH_ONLY_GIFTS = [7, 8, 9]

def generate_positions():
    """Генерирует случайные позиции для 10 коробок"""
    positions = []
    used_positions = set()
    
    for i in range(10):
        while True:
            top = random.randint(5, 75)
            left = random.randint(5, 85)
            pos_key = f"{top}-{left}"
            
            if pos_key not in used_positions:
                positions.append({
                    'top': f"{top}%",
                    'left': f"{left}%"
                })
                used_positions.add(pos_key)
                break
    
    return positions

@lab9.route('/lab9/')
def index():
    # Инициализируем сессию
    if 'lab9_session_id' not in session:
        session['lab9_session_id'] = str(uuid.uuid4())
        session['lab9_opened'] = []
    
    # Если позиции не заданы - генерируем
    if 'lab9_positions' not in session:
        session['lab9_positions'] = generate_positions()
    
    opened = session.get('lab9_opened', [])
    positions = session.get('lab9_positions', [])
    is_auth = current_user.is_authenticated
    
    return render_template('lab9/index.html',
                         opened_boxes=opened,
                         positions=positions,
                         opened_count=len(opened),
                         remaining_count=10 - len(opened),
                         is_auth=is_auth)

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    # Инициализируем сессию если нужно
    if 'lab9_session_id' not in session:
        session['lab9_session_id'] = str(uuid.uuid4())
        session['lab9_opened'] = []
    
    if 'lab9_positions' not in session:
        session['lab9_positions'] = generate_positions()
    
    data = request.get_json()
    
    if not data or 'box_id' not in data:
        return jsonify({
            'success': False,
            'message': 'Ошибка: неверные данные'
        })
    
    box_id = data['box_id']
    
    # Проверяем диапазон
    if not isinstance(box_id, int) or box_id < 0 or box_id > 9:
        return jsonify({
            'success': False,
            'message': 'Ошибка: неверный номер коробки'
        })
    
    # Проверка: только для авторизованных
    if box_id in AUTH_ONLY_GIFTS and not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Этот подарок только для авторизованных пользователей!'
        })
    
    opened = session.get('lab9_opened', [])
    
    # Проверяем, не открыта ли уже
    if box_id in opened:
        return jsonify({
            'success': False,
            'message': 'Эта коробка уже открыта!'
        })
    
    # Проверяем лимит в 3 коробки
    if len(opened) >= 3:
        return jsonify({
            'success': False,
            'message': 'Вы уже открыли 3 коробки! Больше нельзя.'
        })
    
    # Открываем коробку
    opened.append(box_id)
    session['lab9_opened'] = opened
    
    # Получаем поздравление и картинку
    congratulation = CONGRATULATIONS[box_id]
    gift_image = GIFT_IMAGES[box_id]
    
    # Обновляем счетчики
    opened_count = len(opened)
    remaining_count = 10 - opened_count
    
    return jsonify({
        'success': True,
        'congratulation': congratulation,
        'gift_image': f"/static/lab9/{gift_image}",
        'box_id': box_id,
        'opened_count': opened_count,
        'remaining_count': remaining_count,
        'can_open': 3 - opened_count
    })

@lab9.route('/lab9/reset_all', methods=['POST'])
@login_required
def reset_all():
    """Кнопка 'Дед Мороз' - сброс всех коробок для авторизованного пользователя"""
    # Сбрасываем сессию для этого пользователя
    session.pop('lab9_opened', None)
    session.pop('lab9_positions', None)
    session.pop('lab9_session_id', None)
    
    # Создаем новую сессию
    session['lab9_session_id'] = str(uuid.uuid4())
    session['lab9_opened'] = []
    session['lab9_positions'] = generate_positions()
    
    return jsonify({
        'success': True,
        'message': '🎅 Дед Мороз наполнил все коробки снова!'
    })