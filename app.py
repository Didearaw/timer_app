# app.py

import sqlite3
from datetime import datetime, timedelta
import requests
from flask import Flask, render_template, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
import portalocker  # нужно установить: pip install portalocker
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-it'

# --- Настройки Telegram ---
TELEGRAM_TOKEN = ""  # укажите в переменной окружения
TELEGRAM_CHAT_ID = ""  # укажите в переменной окружения

# --- Функция для отправки сообщений в Telegram ---
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"✅ Отправлено в Telegram: {message}")
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")

# --- Работа с базой данных ---
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS timers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            builder_name TEXT NOT NULL,
            start_datetime TEXT NOT NULL,
            days INTEGER DEFAULT 0,
            hours INTEGER DEFAULT 0,
            minutes INTEGER DEFAULT 0,
            notified INTEGER DEFAULT 0,
            last_notified TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Создаём таблицу при первом запуске
init_db()

# --- Вспомогательная функция для форматирования оставшегося времени ---
def format_remaining(seconds):
    if seconds < 0:
        return "Завершён"
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    parts = []
    if days > 0:
        parts.append(f"{days} д")
    if hours > 0:
        parts.append(f"{hours} ч")
    if minutes > 0:
        parts.append(f"{minutes} мин")
    if not parts:
        return "Менее минуты"
    return " ".join(parts)

# --- Основная функция проверки таймеров (с блокировкой и защитой от дублей) ---
def check_timers():
    # Файловая блокировка, чтобы исключить параллельный запуск
    lock_file_path = os.path.join(os.path.dirname(__file__), 'check_timers.lock')
    try:
        lock_file = open(lock_file_path, 'w')
        portalocker.lock(lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
    except portalocker.LockException:
        print("⚠️ Другой экземпляр check_timers уже выполняется, пропускаем.")
        return
    except Exception as e:
        print(f"⚠️ Ошибка блокировки: {e}, продолжаем без блокировки")
        lock_file = None

    try:
        print(f"--- Проверка таймеров в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        conn = get_db_connection()
        # Берём только активные таймеры (notified = 0)
        timers = conn.execute('SELECT * FROM timers WHERE notified = 0').fetchall()
        print(f"Найдено активных таймеров: {len(timers)}")

        for timer in timers:
            timer_id = timer['id']
            builder = timer['builder_name']
            start_str = timer['start_datetime']
            last_notified_str = timer['last_notified']

            # Проверяем, не отправляли ли уведомление за последние 5 минут
            if last_notified_str:
                try:
                    last_time = datetime.fromisoformat(last_notified_str)
                    if (datetime.now() - last_time).total_seconds() < 300:  # 5 минут
                        print(f"Таймер {timer_id}: уведомление уже было отправлено недавно, пропускаем")
                        continue
                except:
                    pass

            try:
                start_time = datetime.fromisoformat(start_str)
            except:
                print(f"Таймер {timer_id}: неверный формат даты {start_str}, пропускаем")
                continue

            duration = timer['days'] * 86400 + timer['hours'] * 3600 + timer['minutes'] * 60
            end_time = start_time + timedelta(seconds=duration)

            if datetime.now() >= end_time:
                print(f"✅ Таймер {timer_id} для {builder} завершён. Отправляем уведомление.")
                message = f"🚨 Таймер для строителя {builder} (ID: {timer_id}) завершен!"
                send_telegram_message(message)

                now_iso = datetime.now().isoformat()
                conn.execute('UPDATE timers SET notified = 1, last_notified = ? WHERE id = ?', (now_iso, timer_id))
                conn.commit()
                print(f"Таймер {timer_id} помечен как отправленный.")
            else:
                remaining = (end_time - datetime.now()).total_seconds()
                print(f"Таймер {timer_id} активен, осталось {int(remaining)} сек.")

        conn.close()
        print("--- Проверка завершена ---")

    finally:
        if lock_file:
            portalocker.unlock(lock_file)
            lock_file.close()

# --- Настройка планировщика (гарантированно одна задача) ---
scheduler = BackgroundScheduler()
scheduler.remove_all_jobs()  # чистим всё
scheduler.add_job(
    func=check_timers,
    trigger="interval",
    seconds=10,               # для теста, потом можно увеличить до 60
    id='check_timers_unique',
    replace_existing=True
)
scheduler.start()

# --- Маршруты веб-приложения ---
@app.route('/')
def index():
    conn = get_db_connection()
    timers = conn.execute('SELECT * FROM timers ORDER BY id DESC').fetchall()
    enriched = []
    now = datetime.now()
    for t in timers:
        tdict = dict(t)
        try:
            start = datetime.fromisoformat(t['start_datetime'])
            duration = t['days']*86400 + t['hours']*3600 + t['minutes']*60
            end = start + timedelta(seconds=duration)
            remaining = (end - now).total_seconds()
            tdict['remaining'] = format_remaining(int(remaining))
        except:
            tdict['remaining'] = '?'
        enriched.append(tdict)
    conn.close()
    return render_template('index.html', timers=enriched)

@app.route('/add', methods=['GET', 'POST'])
def add_timer():
    if request.method == 'POST':
        builder = request.form['builder_name']
        start = request.form['start_datetime']
        days = int(request.form.get('days', 0))
        hours = int(request.form.get('hours', 0))
        minutes = int(request.form.get('minutes', 0))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO timers (builder_name, start_datetime, days, hours, minutes)
            VALUES (?, ?, ?, ?, ?)
        ''', (builder, start, days, hours, minutes))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_timer.html')

@app.route('/delete/<int:id>')
def delete_timer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM timers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Запуск приложения ---
if __name__ == '__main__':
    app.run(debug=True)
