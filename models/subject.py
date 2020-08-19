from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash

class Subject(BaseModel):
    name = pw.CharField(unique=True, null=False)
    