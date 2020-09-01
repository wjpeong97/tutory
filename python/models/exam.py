from models.base_model import BaseModel
from models.subject import Subject
import peewee as pw

class Exam(BaseModel):
    name = pw.CharField(unique=True, null=False)
    date = pw.DateTimeField()
    result = pw.IntegerField()
    file_url = pw.CharField()
    subject = pw.ForeignKeyField(Subject, backref="subjects")

