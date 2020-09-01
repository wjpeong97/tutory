import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.exam import Exam
from playhouse.hybrid import hybrid_property

class Answer(BaseModel):
    exam = pw.ForeignKeyField(Exam, backref="answers", null=False) 
    student = pw.ForeignKeyField(User, backref="answers", on_delete="CASCADE", null=False) 
    submission = pw.TextField(null=False)

    @hybrid_property
    def full_file_url(self):
        from app import app
        return app.config.get("S3_LOCATION") + self.submission

