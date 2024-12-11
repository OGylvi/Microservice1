import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример базы данных задач
tasks = [
    {"id": 1, "user_id": 1, "title": "Купить продукты", "done": False},
]

# Эндпоинт для получения всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

# Эндпоинт для добавления новой задачи
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or "title" not in request.json or "user_id" not in request.json:
        return jsonify({"error": "Invalid input"}), 400

    user_id = request.json["user_id"]

    # Проверяем, существует ли пользователь через User Service
    user_service_url = f'http://127.0.0.1:5001/users/{user_id}'
    user_response = requests.get(user_service_url)

    if user_response.status_code == 404:
        return jsonify({"error": "User not found"}), 404

    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "user_id": user_id,
        "title": request.json["title"],
        "done": False,
    }
    tasks.append(new_task)
    return jsonify({"task": new_task}), 201

# Запуск сервиса
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Используем порт 5000
