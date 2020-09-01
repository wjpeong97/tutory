import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.classroom import Classroom

class Material(BaseModel):
    classroom = pw.ForeignKeyField(Classroom, backref="materials", on_delete="CASCADE", null=False)
    staff = pw.ForeignKeyField(User, backref="materials", on_delete="CASCADE", null=False)
    topic = pw.TextField(null=False)
    name = pw.TextField(null=False)
    link_url = pw.TextField(null=False)
