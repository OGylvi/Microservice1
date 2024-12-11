from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример базы данных пользователей
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

# Эндпоинт для получения всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"users": users})

# Эндпоинт для проверки существования пользователя
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user})

# Эндпоинт для добавления нового пользователя
@app.route('/users', methods=['POST'])
def add_user():
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,  # Генерация нового ID
        "name": request.json["name"]
    }
    users.append(new_user)
    return jsonify({"user": new_user}), 201  # Возвращаем добавленного пользователя с кодом 201

# Запуск сервиса
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Используем порт 5001
