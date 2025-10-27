import peewee

from app.Models.Users import *
from bcrypt import hashpw,gensalt,checkpw

class UserController:

    @classmethod
    def add(
            cls,
            username,
            email,
            password_hash,
            role,
            avatar = None,
            bio = None,
            first_name = None,
            last_name = None,
    ):
        # Хеширование пароля

        hash_password = hashpw(password_hash.encode('utf-8'),gensalt()).decode('utf-8')
        try:
            User.create(
                username = username,
                email = email,
                password_hash = hash_password,
                first_name = first_name,
                last_name = last_name,
                role = role,
                avatar = avatar,
                bio = bio
            )
        except peewee.IntegrityError as error:
            return f'Ошибка {error}'
    # Аунтетификация
    @classmethod
    def auth(cls,login,password):
        user = User.get_or_none(User.username==login)
        if user is not None:
            hash_password = user.password_hash
            if checkpw(password.encode('utf-8'),hash_password.encode('utf-8')):
                return user
        return False

if __name__ == "__main__":
    print(UserController.add(
        username = 'admin22',
        email = 'admin@admin222.ru',
        password_hash = 'admin',
        role = 'admin',
    ))
    u =UserController.auth(
        login='admin',
        password='admin'
    )
    print(u)