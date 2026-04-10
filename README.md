# Fucking Miners — Чат майнеров

Реальный чат для майнеров с синхронизацией сообщений между пользователями.

## Особенности

- **Real-time синхронизация** — все пользователи видят сообщения друг друга
- **Тёмная/светлая тема** — переключение одной кнопкой
- **База пользователей** — регистрация, статистика, онлайн-статусы
- **API сервер** — Flask бэкенд для синхронизации

## Быстрый старт

### 1. Установка зависимостей

```bash
cd mwc-chat
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate на Windows
pip install flask flask-cors
```

### 2. Запуск сервера

```bash
# Запуск API сервера (порт 5004)
./venv/bin/python server.py

# В другом терминале — запуск веб-сервера (порт 5003)
python3 -m http.server 5003
```

### 3. Открыть чат

```
http://localhost:5003
```

## Версии

| Файл | Описание |
|------|----------|
| `index.html` | Версия с сервером (синхронизация) |
| `index-local.html` | Версия без сервера (localStorage) |
| `admin.html` | Админ-панель со статистикой |
| `server.py` | Flask API сервер |

## API Endpoints

```
GET  /api/messages     — Получить сообщения
POST /api/messages     — Отправить сообщение
GET  /api/users        — Получить пользователей
POST /api/users        — Регистрация/логин
GET  /api/stats        — Статистика
```

## Онлайн-версия

После включения GitHub Pages чат будет доступен по адресу:

```
https://fuckfiat.github.io/mwc-chat/
```

**Примечание:** Онлайн-версия работает без сервера (localStorage). Для синхронизации запустите `server.py` локально.

## Технологии

- HTML5 + CSS3 + JavaScript (ES6)
- Flask + Flask-CORS (API)
- LocalStorage API (офлайн-версия)

## Лицензия

MIT