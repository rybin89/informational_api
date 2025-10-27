import datetime
from functools import wraps

import jwt
from flask import request,jsonify




class JWTManger:
    def __init__(self, secret_key,algorithm ='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self,user_id,username,role):
        payload = {
            'user_id' : user_id,
            'username' : username,
            'role' : role,
            'iat' : datetime.datetime.utcnow(),
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload,self.secret_key,algorithm=self.algorithm)
    def verifi_token(self,token):
        try:
            payload = jwt.decode(token,self.secret_key,algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidSignatureError:
            return None
    # Проверка на авторизацию
    # Декоратора
    def requeired(self,f):
        @wraps(f)
        def decorated(*args,**kwargs):
            from app.Contollers.TokenController import TokenController
            auth_token = request.headers.get('Authorization')
            if not auth_token or not auth_token.startswith('Bearer '):
                return jsonify(
                    {
                        'access' : False,
                        'error' : 'Токен остутсвует'
                    }
                ),401
            token = auth_token[7:] # Убираем первые 7 символов ('Bearer ')
            # это токен проверить на is_revoked и expires_at
            is_revoked = TokenController.show(token).is_revoked

            payload = self.verifi_token(token)
            print(is_revoked)
            if not payload or is_revoked:
                return jsonify(
                    {
                        'access': False,
                        'error': 'Токен недействительный или просроченый'
                    }
                ),401
            return f(*args,**kwargs,user = payload,token = token)
        return decorated
    def role_requeired(self,role):
        def decorator(f):
            @wraps(f)
            def decorated(*args,**kwargs):
                user = kwargs['user']
                if user['role'] != role:
                    return jsonify(
                        {
                            'access': False,
                            'error': 'Вход запрещён'
                        }
                    ),401
                return f(*args,**kwargs)
            return decorated
        return decorator




if __name__ == "__main__":
    token = JWTManger('22ISiP')
    new_token = token.create_token(1,'user','user')
    print(new_token)
    print(token.verifi_token(new_token))