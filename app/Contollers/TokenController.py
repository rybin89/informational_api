from app.Models.Token import *
from app.Middleware.Auth import JWTManger
SECRET_KEY = '22ISiP'
jwt_manager = JWTManger(SECRET_KEY)


class TokenController:
    @classmethod
    def add(cls,user_id,username,role):
        token = jwt_manager.create_token(user_id=user_id,username=username,role=role)
        expires_at = datetime.now() + timedelta(hours=24)
        Token.create(token=token,user_id=user_id,expires_at=expires_at)
        return token

    @classmethod
    def show_active_token_user(cls,user_id):
        '''
        Вывод активных токенов
        :Params user_id: ИД пользователя
        :Returns:
            список активных токенов пользователя
        '''
        return Token.select().where(
            Token.user_id == user_id,
            Token.is_revoked == False
        )
    # Прокси методы
    @classmethod
    def requeired(cls, f):

        return jwt_manager.requeired(f)

    @classmethod
    def role_requeired(cls, role):
        return jwt_manager.role_requeired(role)
    # Отозвать токен
    @classmethod
    def revoked(cls,token):
        Token.update(is_revoked=True,revoked_at=datetime.now()).where(Token.token == token).execute()

    @classmethod
    def show(cls,token):
        return Token.get_or_none(Token.token == token)

