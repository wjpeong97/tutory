import peewee as pw
from models.base_model import BaseModel
from models.staff import Staff
from models.subject import Subject

class Classroom(BaseModel):
    year = pw.IntegerField(null=False)
    staff = pw.ForeignKeyField(Staff, backref="classes")
    subject = pw.ForeignKeyField(Subject, backref="classes")