import peewee as pw
from models.base_model import BaseModel
from models.user import User

class Assignment(BaseModel):
    student = pw.ForeignKeyField(User, backref="assignments")
    staff = pw.ForeignKeyField(User, backref="assignments")
    homework = pw.TextField(null=True)
    submission = pw.TextField(null=True)