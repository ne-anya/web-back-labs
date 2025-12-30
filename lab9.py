from flask import Blueprint, render_template, session, jsonify, request
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

# 10 картинок подарков (которые внутри коробок)
GIFT_IMAGES = [
    "gift1.jpg", "gift2.jpg", "gift3.jpg", "gift4.jpg", "gift5.jpg",
    "gift6.jpg", "gift7.jpg", "gift8.jpg", "gift9.jpg", "gift10.jpg"
]

@lab9.route('/lab9/')
def index():
    # Инициализируем сессию для этой лабораторной
    if 'lab9_session_id' not in session:
        session['lab9_session_id'] = str(uuid.uuid4())
        session['lab9_opened'] = []  # какие коробки уже открыты
        session['lab9_positions'] = []  # позиции коробок
    
    # Если позиции не заданы - генерируем случайные
    if not session['lab9_positions']:
        positions = []
        # Уникальные позиции, чтобы коробки не перекрывались
        used_positions = set()
        
        for i in range(10):
            while True:
                top = random.randint(5, 75)  # от 5% до 75%
                left = random.randint(5, 85)  # от 5% до 85%
                pos_key = f"{top}-{left}"
                
                if pos_key not in used_positions:
                    positions.append({
                        'top': f"{top}%",
                        'left': f"{left}%"
                    })
                    used_positions.add(pos_key)
                    break
        
        session['lab9_positions'] = positions
    
    opened = session['lab9_opened']
    positions = session['lab9_positions']
    
    return render_template('lab9/index.html',
                         opened_boxes=opened,
                         positions=positions,
                         opened_count=len(opened),
                         remaining_count=10 - len(opened))

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    # Проверяем сессию
    if 'lab9_session_id' not in session:
        session['lab9_session_id'] = str(uuid.uuid4())
        session['lab9_opened'] = []
    
    data = request.get_json()
    
    # Проверяем данные
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
    
    opened = session['lab9_opened']
    
    # 1. Проверяем, не открыта ли уже эта коробка
    if box_id in opened:
        return jsonify({
            'success': False,
            'message': 'Эта коробка уже открыта!'
        })
    
    # 2. Проверяем лимит в 3 коробки
    if len(opened) >= 3:
        return jsonify({
            'success': False,
            'message': 'Вы уже открыли 3 коробки! Больше нельзя.'
        })
    
    # 3. Открываем коробку
    opened.append(box_id)
    session['lab9_opened'] = opened
    
    # 4. Получаем поздравление и картинку подарка
    congratulation = CONGRATULATIONS[box_id]
    gift_image = GIFT_IMAGES[box_id]
    
    # 5. Обновляем счетчики
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