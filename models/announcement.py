import peewee as pw
from models.base_model import BaseModel
from models.user import User

class Announcement(BaseModel):
    staff = pw.ForeignKeyField(User, backref="announcements")
    post = pw.TextField()