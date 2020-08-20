import peewee as pw
import re
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from models.base_model import BaseModel
# from models.student import Student

class Staff(UserMixin,BaseModel):
    full_name = pw.CharField(unique=True, null=False)
    identity_card = pw.IntegerField(unique=True, null=False)
    password_hash = pw.TextField(null=False)
    email = pw.CharField(unique=True, null=False)
    password = None
    image_url = pw.TextField(null=True)    
    
    # @hybrid_property
    # def full_image_path(self):
    #     from app import app
    #     if self.image_path:
    #         return app.config.get("S3_LOCATION") + self.image_path
    #     else:
    #         return app.config.get("S3_LOCATION") + "blank-profile-picture.png"

    def validate(self):
        # Email should be unique
        # existing_student_email = Student.get_or_none(Student.email==self.email)
        existing_staff_email = Staff.get_or_none(Staff.email==self.email)
        if existing_staff_email:
            self.errors.append(f"This email {self.email} has already existed!")
        
        # Name should be unique
        # existing_student_full_name = Student.get_or_none(Student.full_name==self.full_name)
        existing_staff_full_name = Staff.get_or_none(Staff.full_name==self.full_name)
        if existing_staff_full_name:
            self.errors.append(f"This name {self.full_name} has already existed!")
        
        # identity card should be unique
        # existing_student_identity_card = Student.get_or_none(Student.identity_card==self.identity_card)
        existing_staff_identity_card = Staff.get_or_none(Staff.identity_card==self.identity_card)
        if existing_staff_identity_card:
            self.errors.append(f"The IC number {self.identity_card} has already existed!")

        # Password should be longer than 6 characters
        if self.password:
            if len(self.password) <= 6:
                self.errors.append("Password is less than 6 characters")
            # Password should have both uppercase and lowercase characters
            # Password should have at least one special character (REGEX comes in handy here)
            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[\[ \] \* \$ \% \^ \& \# ]", self.password)

            if has_lower and has_upper and has_special:
                self.password_hash = generate_password_hash(self.password)
            else:
                self.errors.append("Password either does not have upper, lower or special characters!")