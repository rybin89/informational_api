from datetime import datetime

from app.Models.Base import *


class User(Base):
    id = PrimaryKeyField()
    username = CharField(unique=True, max_length=50)
    email = CharField(unique=True, max_length=100)
    password_hash = CharField(max_length=255)
    first_name = CharField(max_length=50, null=True)
    last_name = CharField(max_length=50, null=True)
    role = CharField(choices=['admin', 'editor', 'author', 'user'], default='user')
    avatar = CharField(max_length=255, null=True)
    bio = TextField(null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


if __name__ == "__main__":
    connect_db().create_tables([User])