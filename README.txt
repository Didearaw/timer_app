⏰ Таймер уведомлений в Telegram



Веб-приложение для отслеживания таймеров. Когда таймер истекает, приходит сообщение в Telegram.



🚀 Возможности



- Добавление таймеров через веб-интерфейс

- Обратный отсчёт в реальном времени

- Автоматическая отправка уведомлений в Telegram

- Защита от дублирования сообщений

- Работает на PythonAnywhere (бесплатно)



🛠 Установка и запуск



Локально



1. Клонируйте репозиторий:
  git clone https://github.com/ваш-логин/timer_app.git
  cd timer_app

2. Создайте виртуальное окружение:
  python -m venv venv
  source venv/bin/activate      # для Linux/Mac
  venv\Scripts\activate          # для Windows

3. Установите зависимости:
   pip install -r requirements.txt

4. Запустите приложение:
   python app.py

5. Откройте в браузере:
   http://127.0.0.1:5000


Настройка Telegram
1. Создайте бота у @BotFather
2. Получите токен и ваш chat_id
3. В файле app.py укажите:
   TELEGRAM_TOKEN = "ваш_токен"
   TELEGRAM_CHAT_ID = "ваш_chat_id"


Деплой на PythonAnywhere
Подробная инструкция в Wiki.

📦 Зависимости
Flask
requests
APScheduler
portalocker

