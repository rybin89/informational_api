from datetime import datetime
from app.Models.Base import *
from app.Models.Category import Category
from app.Models.Users import User


class Article(Base):
    id = PrimaryKeyField()
    title = CharField(max_length=255)
    slug = CharField(unique=True, max_length=255)
    excerpt = TextField(null=True) # краткое содержание
    content = TextField()
    featured_image = CharField(max_length=255, null=True) # путь к изображению
    status = CharField(choices=['draft', 'published', 'archived'], default='draft')
    views = IntegerField(default=0) # количество просмотров
    reading_time = IntegerField(default=0)  # в минутах
    author = ForeignKeyField(User, backref='articles')
    category = ForeignKeyField(Category, backref='articles', null=True)
    published_at = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


if __name__ == "__main__":
    connect_db().create_tables([Article])