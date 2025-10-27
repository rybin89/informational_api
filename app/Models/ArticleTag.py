from datetime import datetime

from app.Models.Article import Article
from app.Models.Base import *
from app.Models.Tag import Tag


class ArticleTag(Base):
    id = PrimaryKeyField()
    article = ForeignKeyField(Article, backref='articletags')
    tag = ForeignKeyField(Tag, backref='articletags')

if __name__ == "__main__":
    connect_db().create_tables([ArticleTag])