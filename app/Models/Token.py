from datetime import datetime, timedelta

from app.Models.Base import *
from app.Models.Users import User


class Token(Base):
    id = PrimaryKeyField()
    token = CharField()
    user_id = ForeignKeyField(User, backref='users')
    expires_at = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    revoked_at = DateTimeField(default=(created_at + timedelta(hours = 24)))
    is_revoked = BooleanField(default=False)


if __name__ == "__main__":
    connect_db().create_tables([Token])