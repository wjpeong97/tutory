import peewee as pw
from models.base_model import BaseModel
from models.user import User

class Activities(BaseModel):
    full_name = pw.CharField(unique=False, null=False)
    identity_card = pw.IntegerField(unique=False, null=False)
    title = pw.CharField(null=False)
    post = pw.TextField(null=False)