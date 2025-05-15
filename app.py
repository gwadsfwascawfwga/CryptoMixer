from flask import Flask, render_template, request, session, jsonify
from datetime import datetime
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DATABASE'] = 'cryptomixer.db'

def init_db():
    with app.app_context():
        db = sqlite3.connect(app.config['DATABASE'])
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            registered_at DATETIME
        )''')
        
        db.execute('''CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            coin TEXT,
            address TEXT,
            timestamp DATETIME,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        db.commit()

init_db()

def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user and user['password'] == hash_password(password):
        return user
    return None

@app.route('/')
def index():
    operations = []
    if 'user_id' in session:
        db = get_db()
        operations = db.execute('''SELECT * FROM operations 
                                 WHERE user_id = ? 
                                 ORDER BY timestamp DESC LIMIT 10''',
                              (session['user_id'],)).fetchall()
    
    return render_template('index.html',
                         username=session.get('username'),
                         registered_at=session.get('registered_at'),
                         operations=operations)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    action = data.get('action')
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    response = {'status': 'error', 'message': ''}

    try:
        if action == 'login':
            user = authenticate_user(username, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['registered_at'] = user['registered_at']
                response.update({
                    'status': 'success',
                    'username': user['username'],
                    'registered_at': user['registered_at']
                })
            else:
                response['message'] = "Неверные учетные данные"
        
        elif action == 'register':
            if db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
                response['message'] = "Пользователь уже существует"
            else:
                hashed_pw = hash_password(password)
                db.execute('INSERT INTO users (username, password, registered_at) VALUES (?, ?, ?)',
                          (username, hashed_pw, datetime.now().strftime('%Y-%m-%d %H:%M')))
                db.commit()
                response['status'] = 'success'
        
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error in auth: {str(e)}")
        response['message'] = "Ошибка сервера"
        return jsonify(response)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'status': 'success'})

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Требуется авторизация'})
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    response = {'status': 'error', 'message': ''}

    if user and user['password'] == hash_password(current_password):
        db.execute('UPDATE users SET password = ? WHERE id = ?',
                  (hash_password(new_password), session['user_id']))
        db.commit()
        response['status'] = 'success'
    else:
        response['message'] = "Неверный текущий пароль"
    
    return jsonify(response)

@app.route('/mix', methods=['POST'])
def mix():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Требуется авторизация'}), 401
    
    try:
        # Получаем данные из JSON
        data = request.get_json()
        amount = float(data['amount'])
        coin = data['coin']
        address = data['address']
        
        if amount <= 0:
            return jsonify({'status': 'error', 'message': 'Сумма должна быть больше нуля'}), 400
        
        # Сохраняем операцию в БД
        db = get_db()
        db.execute('''INSERT INTO operations 
                   (user_id, amount, coin, address, timestamp)
                   VALUES (?, ?, ?, ?, ?)''',
                (session['user_id'], amount, coin, address, datetime.now().strftime('%Y-%m-%d %H:%M')))
        db.commit()
        
        return jsonify({'status': 'success', 'message': 'Операция успешно запущена'})
        
    except (KeyError, ValueError, TypeError) as e:
        app.logger.error(f"Ошибка в данных: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Некорректные данные'}), 400
    except Exception as e:
        app.logger.error(f"Ошибка сервера: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Внутренняя ошибка сервера'}), 500

if __name__ == '__main__':
    app.run(debug=True)
