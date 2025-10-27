from datetime import datetime

from app.Models.Article import Article
from app.Models.Base import *
from app.Models.Users import User


class Comment(Base):
    id = PrimaryKeyField()
    content = TextField()
    author = ForeignKeyField(User, backref='comments')
    article = ForeignKeyField(Article, backref='comments')
    parent = ForeignKeyField('self', null=True, backref='replies')
    is_approved = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

if __name__ == "__main__":
    connect_db().create_tables([Comment])