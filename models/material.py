import peewee as pw
from models.base_model import BaseModel
from models.classroom import Classroom
from models.exam import Exam

class Material(BaseModel):
    classroom = pw.ForeignKeyField(Classroom, backref="materials")
    exam = pw.ForeignKeyField(Exam, backref="materials")