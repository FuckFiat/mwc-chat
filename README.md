# Fucking Miners — Терминальный чат для майнеров

Веб-чат в стиле Zulip Terminal для майнеров криптовалют.

## 🚀 Возможности

- **3-колоночный макет** — навигация, чат, пользователи
- **Тёмная/Светлая тема** — переключение кликом по ⚡
- **JetBrains Mono** — моноширинный шрифт
- **Свайп для ответов** — как в Telegram
- **Разные цвета** — пастельные для каждого пользователя
- **Каналы** — переключение между каналами
- **Горячие клавиши** — [a], [p], [@], [q], [w]
- **Real-time синхронизация** — polling каждые 1 сек
- **Сохранение данных** — пользователи и сообщения на диске
- **Ответы на сообщения** — свайп влево или правый клик

## 📦 Файлы

| Файл | Описание |
|------|----------|
| `chat.html` | Веб-интерфейс (клиент) |
| `index.html` | Локальная версия (localStorage) |
| `server-production.py` | Flask API сервер |
| `start.sh` | Скрипт запуска |
| `admin.html` | Админ-панель |

## 🛠️ Установка

### 1. Сервер (VPS)

```bash
# Клонировать репозиторий
git clone https://github.com/FuckFiat/mwc-chat.git
cd mwc-chat

# Установить зависимости
pip3 install flask flask-cors

# Скопировать файлы
sudo mkdir -p /var/www/fucking-miners
sudo cp server-production.py /var/www/fucking-miners/server.py
sudo cp chat.html /var/www/fucking-miners/chat.html

# Создать systemd service
sudo cat > /etc/systemd/system/fucking-miners.service << EOF
[Unit]
Description=Fucking Miners Chat Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/fucking-miners
ExecStart=/usr/bin/python3 /var/www/fucking-miners/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Запустить
sudo systemctl daemon-reload
sudo systemctl enable fucking-miners
sudo systemctl start fucking-miners
```

### 2. Nginx

```nginx
server {
    listen 80;
    server_name chat.fuckfiat.com 95.140.148.73;
    
    location /api/ {
        proxy_pass http://127.0.0.1:5004;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        root /var/www/fucking-miners;
        index chat.html;
        try_files $uri $uri/ /chat.html;
    }
}
```

## 🌐 URL

| Сервис | URL |
|--------|-----|
| **Чат** | http://95.140.148.73/ |
| **API** | http://95.140.148.73:5004/ |
| **GitHub** | https://github.com/FuckFiat/mwc-chat |

## 🎨 Темы

| Тема | Логотип | Цвета |
|------|---------|-------|
| **Тёмная** | ⚡ | Тёмно-серый фон, пастельные цвета |
| **Светлая** | ☀️ | Белый фон, яркие контрастные цвета |

**Переключение:** клик по логотипу ⚡/☀️

## 🖐️ Свайп

| Действие | Результат |
|----------|-----------|
| **Свайп влево** | Цитата в поле ввода |
| **Правый клик** | Меню: Ответить, Личное, Копировать |

## 📋 API Endpoints

```
GET  /              — Health check
GET  /api/messages  — Получить сообщения
POST /api/messages  — Отправить сообщение
GET  /api/users     — Получить пользователей
POST /api/users     — Регистрация
GET  /api/stats     — Статистика
```

## ⌨️ Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| `Enter` | Отправить сообщение |
| `Shift+Enter` | Новая строка |
| `q` | Фокус на поиск |
| `w` | Поиск пользователей |

## 🎨 Цвета пользователей

| Класс | Тёмная тема | Светлая тема |
|-------|-------------|--------------|
| `user-color-0` | `#a8d8ea` | `#2196F3` |
| `user-color-1` | `#aa96da` | `#9C27B0` |
| `user-color-2` | `#fcbad3` | `#E91E63` |
| `user-color-3` | `#a8e6cf` | `#4CAF50` |
| `user-color-4` | `#ffd3b6` | `#FF9800` |
| `user-color-5` | `#dcedc1` | `#8BC34A` |
| `user-color-6` | `#c9b1ff` | `#673AB7` |
| `user-color-7` | `#b5ead7` | `#009688` |
| `user-color-8` | `#ffc6ff` | `#F50057` |
| `user-color-9` | `#bdb2ff` | `#3F51B5` |

## 📊 Данные

Данные сохраняются в:
```
/var/www/fucking-miners/data/chat_data.json
```

Структура:
```json
{
  "users": {
    "username": {
      "password": "hash",
      "avatar": "N",
      "online": true,
      "createdAt": 1234567890,
      "lastSeen": 1234567890,
      "messageCount": 42
    }
  },
  "messages": [
    {
      "user": "username",
      "text": "Привет!",
      "time": 1234567890
    }
  ]
}
```

## 🛡️ Безопасность

- Пароли хешируются перед сохранением
- CORS разрешён для всех доменов
- Нет аутентификации сессий (простой чат)

## 📝 Лицензия

MIT