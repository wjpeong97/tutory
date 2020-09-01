import peewee as pw
from models.base_model import BaseModel
from models.material import Material
from models.user import User

class Exam(BaseModel):
    material = pw.ForeignKeyField(Material, backref="exams",on_delete="CASCADE", null=False) # Will need to be hidden @ material page (e.g. topic = "exam") 
    staff = pw.ForeignKeyField(User, backref="exams", on_delete="CASCADE", null=False) 
