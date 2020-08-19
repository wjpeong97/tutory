import peewee as pw
from models.base_model import BaseModel
from models.student import Student
from models.staff import Staff

class Assignment(BaseModel):
    student = pw.ForeignKeyField(Student, backref="assignments")
    staff = pw.ForeignKeyField(Staff, backref="assignments")
    homework = pw.TextField(null=True)
    submission = pw.TextField(null=True)