from datetime import datetime

from app.Models.Base import *

class Category(Base):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    slug = CharField(unique=True, max_length=100)
    description = TextField(null=True)
    parent = ForeignKeyField('self', null=True, backref='children')
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
if __name__ == "__main__":
    connect_db().create_tables([Category])