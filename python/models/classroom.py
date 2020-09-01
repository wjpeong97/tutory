import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.subject import Subject

class Classroom(BaseModel):
    year = pw.IntegerField(null=False)
    staff = pw.ForeignKeyField(User, backref="classes")
    subject = pw.ForeignKeyField(Subject, backref="classes")