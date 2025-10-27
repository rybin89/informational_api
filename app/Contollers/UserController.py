import peewee

from app.Models.Users import *
from bcrypt import hashpw, gensalt, checkpw


class UserController:

    @classmethod
    def add(
            cls,
            username,
            email,
            password_hash,
            role="user",
            avatar=None,
            bio=None,
            first_name=None,
            last_name=None,
    ):
        # Хеширование пароля

        hash_password = hashpw(password_hash.encode('utf-8'), gensalt()).decode('utf-8')
        try:
            choices = ['admin', 'editor', 'author', 'user']
            if role in choices:
                User.create(
                        username=username,
                        email=email,
                        password_hash=hash_password,
                        first_name=first_name,
                        last_name=last_name,
                        role=role,
                        avatar=avatar,
                        bio=bio
                    )
            elif role == '':
                    User.create(
                        username=username,
                        email=email,
                        password_hash=hash_password,
                        first_name=first_name,
                        last_name=last_name,
                        avatar=avatar,
                        bio=bio)
            else:
                return f'Ошибка. Роль {role} не найдена'

        except peewee.IntegrityError as error:
            return f'Ошибка {error}'

    # Аунтетификация
    @classmethod
    def auth(cls, login, password):
        user = User.get_or_none(User.username == login)
        if user is not None:
            hash_password = user.password_hash
            if checkpw(password.encode('utf-8'), hash_password.encode('utf-8')):
                return user
        return False
    @classmethod
    def get_user(cls, username):
        return User.get_or_none(User.username == username)
    @classmethod
    def get(cls):
        return User.select()
    @classmethod
    def show_id(cls, id):
        return User.get_or_none(id)
    @classmethod
    def update(cls, id, **kwargs):
        if kwargs:
            if 'password_hash' in kwargs:
                hash_password = hashpw(kwargs['password_hash'].encode('utf-8'), gensalt()).decode('utf-8')
                kwargs['password_hash'] = hash_password
            User.update(**kwargs).where(User.id == id).execute()
            return User.get_or_none(id)
        else:
            return False
    @classmethod
    def delete(cls, id):
        if id != 2: # id админа
            User.delete().where(User.id == id).execute()

if __name__ == "__main__":
    print(UserController.add(
        username='admasdsdfsdfasin22',
        email='sdf@admin222.ru',
        password_hash='adasdmin',
        role='dsf',
    ))
    u = UserController.auth(
        login='admin',
        password='admin'
    )
    print(u)
    print(UserController.get_user('ivasdffs222'))
    print(UserController.show_id(2))
    print(UserController.update(16,username='WWW',email='WWW@WWW.ru'))