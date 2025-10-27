from flask import Blueprint, Flask, jsonify, request

from app.Contollers.TokenController import TokenController
from app.Contollers.UserController import UserController

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@TokenController.requeired
@TokenController.role_requeired('admin')
def register(user):
    '''
    маршрут для создания пользователей
    :param user:
    :return:
    username,
             email,
             password_hash,
             first_name,
             last_name,
             role,
             avatar,
             bio
    '''
    data_user = request.get_json()

    new_user = UserController.add(
        data_user['username'],
        data_user['email'],
        data_user['password_hash'],
        data_user['role'],
        data_user['avatar'],
        data_user['bio'],
        data_user['first_name'],
        data_user['last_name']
    )
    if new_user is not None:
        return jsonify(
            {
                "success": False,
                "error": new_user
            }

        ), 422
    return jsonify(
        {
            "success": True,
            "message": "Пользователь создан",
            "user": {
                'username': data_user['username'],
                'email': data_user['email'],
                'password_hash': data_user['password_hash'],
                'role': data_user['role'],
                'avatar': data_user['avatar'],
                'bio': data_user['bio'],
                'first_name': data_user['first_name'],
                'last_name': data_user['last_name']
            }

        }
    ),201


@auth_bp.route('/login', methods=['POST'])
def login():
    data_user = request.get_json()
    user = UserController.auth(data_user['login'], data_user['password'])
    print(user)
    if user:
        token = TokenController.add(user.id, user.username, user.role)
        return jsonify(
            {
                "success": True,
                "token": token,
                "user_id": user.id,
                "username": user.username,
                "role": user.role
            }
        ), 200
    return jsonify(
        {
            "success": False,
            "error": "Неверный логин или пароль"
        }
    ), 401
