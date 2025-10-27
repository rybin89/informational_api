from flask import Blueprint, request, jsonify

from app.Contollers.TokenController import TokenController
from app.Contollers.UserController import UserController

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['GET'])
@TokenController.requeired
@TokenController.role_requeired('admin')
def get_users(user, token):
    users = UserController.get()
    list = []
    for user in users:
        list.append({
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'avatar': user.avatar,
            'bio': user.bio,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at
        })

    return jsonify(list), 200


@users_bp.route('/<int:id>', methods=['GET'])
@TokenController.requeired
@TokenController.role_requeired('admin')
def get_user(user, token, id):
    user = UserController.show_id(id)
    return jsonify({
        'access': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'avatar': user.avatar,
            'bio': user.bio,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at}
    }), 200

@users_bp.route('/<int:id>', methods=['PUT'])
@TokenController.requeired
@TokenController.role_requeired('admin')
def update_user(user, token, id):

