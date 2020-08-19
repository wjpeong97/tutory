import peewee as pw
from models.base_model import BaseModel
from models.staff import Staff

class Announcement(BaseModel):
    staff = pw.ForeignKeyField(Staff, backref="announcements")
    post = pw.TextField()