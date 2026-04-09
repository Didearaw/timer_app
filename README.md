```markdown
# ⏰ Timer Telegram Notifier

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> Веб-приложение для отслеживания таймеров с отправкой уведомлений в Telegram. Идеально подходит для напоминаний о событиях, контроле времени строителей или любых других задач, где важно не пропустить дедлайн.

## 🚀 Возможности

- ✅ **Добавление таймеров** через простой веб-интерфейс
- ⏳ **Обратный отсчёт** в реальном времени (обновляется при загрузке страницы)
- 🤖 **Автоматические уведомления** в Telegram при истечении таймера
- 🛡️ **Защита от дублирования** — сообщение приходит ровно один раз
- 🌍 **Работает на бесплатном хостинге** (PythonAnywhere, Render и др.)
- 🗄️ **Локальное хранение** данных в SQLite

## 🖼️ Скриншот

*(Добавьте сюда скриншот интерфейса, например:)*  
![Интерфейс приложения](screenshot.png)

## 📦 Установка и запуск

### Локально

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/didearaw/timer_app.git
   cd timer_app
   ```

2. **Создайте виртуальное окружение**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте Telegram** (см. раздел ниже)

5. **Запустите приложение**
   ```bash
   python app.py
   ```

6. **Откройте в браузере** → `http://127.0.0.1:5000`

## 🤖 Настройка Telegram бота

1. Найдите в Telegram [@BotFather](https://t.me/BotFather)
2. Создайте нового бота командой `/newbot` и получите **токен** (например, `123456:ABC-DEF...`)
3. Узнайте свой `chat_id`. Самый простой способ:
   - Отправьте боту любое сообщение
   - Перейдите по ссылке: `https://api.telegram.org/bot<ТОКЕН>/getUpdates`
   - В ответе найдите `"chat":{"id": ...}`
4. **Безопасный способ хранения токена** (рекомендуется):
   - Создайте файл `.env` в корне проекта:
     ```
     TELEGRAM_TOKEN=ваш_токен
     TELEGRAM_CHAT_ID=ваш_id
     ```
   - Установите `pip install python-dotenv`
   - В `app.py` добавьте:
     ```python
     from dotenv import load_dotenv
     load_dotenv()
     TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
     TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
     ```
   - **Важно:** Не публикуйте `.env` в Git (он уже добавлен в `.gitignore`)

Если вы не используете `.env`, можно прямо в `app.py` указать токен, но **никогда не выкладывайте его на GitHub**!

## 🌐 Деплой на PythonAnywhere

1. Зарегистрируйтесь на [PythonAnywhere](https://www.pythonanywhere.com) (бесплатный аккаунт)
2. Загрузите файлы проекта (кроме `.env` и `database.db`)
3. В разделе **Web** настройте WSGI-файл, указав путь к `app.py`
4. Установите зависимости через консоль: `pip install -r requirements.txt`
5. **Задайте переменные окружения** `TELEGRAM_TOKEN` и `TELEGRAM_CHAT_ID` в разделе **Web → Environment variables**
6. Нажмите **Reload**

> **Важно:** На бесплатном тарифе сайт «засыпает» при отсутствии активности, но фоновый планировщик продолжает работать, и уведомления будут приходить.

## 📋 Зависимости

Все зависимости перечислены в `requirements.txt`:
- `Flask` — веб-фреймворк
- `requests` — для отправки запросов к Telegram API
- `APScheduler` — для фоновой проверки таймеров
- `portalocker` — для предотвращения одновременного запуска нескольких проверок

## 🤝 Внесение вклада

Если вы нашли ошибку или хотите улучшить проект:
1. Создайте форк репозитория
2. Сделайте свои изменения
3. Отправьте пул-реквест

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## 🙏 Благодарности

Создано при поддержке сообщества.  
Если проект вам помог — поставьте ⭐ на GitHub!
```
