from app.database import *

class Base(Model):
    class Meta:
        database = connect_db()
