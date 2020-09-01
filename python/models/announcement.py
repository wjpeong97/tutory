import peewee as pw
from models.base_model import BaseModel
from models.user import User

class Announcement(BaseModel):
    staff = pw.ForeignKeyField(User, on_delete="CASCADE", null=False)
    title = pw.CharField(null=False)
    post = pw.TextField(null=False)