from app.Models.Users import User


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

        User.create(
            username = username,
            email = email,
            password_hash = password_hash,
            first_name = first_name,
            last_name = last_name,
            role = role,
            avatar = avatar,
            bio = bio
        )
