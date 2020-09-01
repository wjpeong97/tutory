from models.base_model import BaseModel
from models.subject import Subject
from models.user import User
import peewee as pw

class Grade(BaseModel):
    student = pw.ForeignKeyField(User, unique=False, null=False, on_delete="CASCADE")
    year = pw.IntegerField(null=False)
    subject = pw.ForeignKeyField(Subject, null=False, on_delete="CASCADE")
    grade = pw.IntegerField(null=False)

    def validate(self):
        duplicate_entry = Grade.get_or_none(Grade.subject==self.subject, Grade.student==self.student)
        if duplicate_entry and self.id != duplicate_entry.id: 
        # GRADE ROUTE - def create validation result will be False(its a create so there is never a duplicate entry) and False(there is no self.id to begin with and no duplicate id as well)
        # GRADE ROUTE - def edit(id) validation result will be True(there is a duplicate entry) and False(assuming the grade to edit is 7 and the duplicated entry is 7 hence 7!=7 is false - intentional)
            self.errors.append('There is existing grade!')
            
    class Meta:
        indexes = (
            # create a unique on student/subject/year
            (('student', 'subject'), True),
        )