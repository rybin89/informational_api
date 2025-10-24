from flask import Blueprint, Flask, jsonify, request

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

auth_bp.route('/register', methods=['POST'])


def register(username,
             email,
             password_hash,
             first_name,
             last_name,
             role,
             avatar,
             bio):
    pass

