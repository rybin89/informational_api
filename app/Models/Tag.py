from datetime import datetime

from app.Models.Base import *

class Tag(Base):
    id = PrimaryKeyField()
    name = CharField(max_length=50)
    slug = CharField(unique=True, max_length=50)

if __name__ == "__main__":
    connect_db().create_tables([Tag])