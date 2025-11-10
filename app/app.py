from flask import Flask
from redis import Redis
import os

app = Flask(__name__)
# Обратите внимание: мы используем имя сервиса 'redis' как хост,
# а не 'localhost'. Docker сам разберется, как их соединить.
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    # Увеличиваем счетчик в Redis на 1 при каждом заходе
    count = redis.incr('hits')
    return f'Hello from Docker! This page has been visited {count} times.\n'

if __name__ == "__main__":
    # Запускаем приложение на порту 5000, доступное для всех
    app.run(host="0.0.0.0", port=5000, debug=True)