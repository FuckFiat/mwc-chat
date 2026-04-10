#!/bin/bash
# Запуск Fucking Miners Chat

cd "$(dirname "$0")"

echo "=== Fucking Miners Chat ==="
echo ""

# Проверка venv
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
    source venv/bin/activate
    pip install flask flask-cors --quiet
else
    source venv/bin/activate
fi

# Запуск API сервера
echo "Запуск API сервера (порт 5004)..."
venv/bin/python server.py &
SERVER_PID=$!

# Ожидание запуска
sleep 2

# Проверка
if curl -s http://localhost:5004/api/stats > /dev/null; then
    echo "✅ API сервер запущен"
else
    echo "❌ Ошибка запуска API сервера"
    exit 1
fi

# Запуск HTTP сервера
echo "Запуск HTTP сервера (порт 5003)..."
python3 -m http.server 5003 &
HTTP_PID=$!

sleep 1

echo ""
echo "=== Готово! ==="
echo ""
echo "Чат: http://localhost:5003"
echo "API: http://localhost:5004"
echo "Админка: http://localhost:5003/admin.html"
echo ""
echo "Нажмите Ctrl+C для остановки..."

# Ожидание
trap "kill $SERVER_PID $HTTP_PID 2>/dev/null; exit" INT TERM
wait