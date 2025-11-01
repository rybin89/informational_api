from flask import Blueprint, Flask, jsonify, request

from app.Contollers.TokenController import TokenController
from app.Contollers.UserController import UserController

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@TokenController.requeired
@TokenController.role_requeired('admin')
def register(user,token):
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
    if data_user is None:
        return jsonify(
            {
                "success": False,
                "error": "нет данных"
            }

        ), 422

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
    if data_user['role'] == '':
        data_user['role'] = 'user'
    user = UserController.get_user(data_user['username'])
    return jsonify(
        {
            "success": True,
            "message": "Пользователь создан",
            "user": {
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'avatar': user.avatar,
                'bio': user.bio,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'created_at': user.created_at
            }

        }
    ),201

@auth_bp.route('/login', methods=['POST'])
def login():
    data_user = request.get_json()
    user = UserController.auth(data_user['login'], data_user['password'])

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

@auth_bp.route('/logout', methods=['POST'])
@TokenController.requeired
def logout_user(user,token):

    TokenController.revoked(token)

    return jsonify(
        {
            "success": True,
            "error": "Успешный выход из системы"
        }
    ), 200

@auth_bp.route('/me', methods=['GET'])
@TokenController.requeired
def me(user,token):
    user = UserController.get_user(user['username'])
    return jsonify(
            {
                "success": True,
                "user": {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'bio': user.bio,
                    'avatar': user.avatar,
                    'role': user.role,
                    'is_active': user.is_active,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at,

                }
            }
        ), 200