import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.classroom import Classroom

class Assignment(BaseModel):
    classroom = pw.ForeignKeyField(Classroom, backref="assignments", on_delete="CASCADE", null=False)
    student = pw.ForeignKeyField(User, backref="assignments", on_delete="CASCADE", null=False)
    topic = pw.TextField(null=False)
    name = pw.TextField(null=False)
    link_url = pw.TextField(null=False)