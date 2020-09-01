import peewee as pw
import re
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from models.base_model import BaseModel

class User(UserMixin,BaseModel):
    full_name = pw.CharField(unique=True, null=False)
    identity_card = pw.IntegerField(unique=True, null=False)
    password_hash = pw.TextField(null=False)
    email = pw.CharField(unique=True, null=False)
    password = None
    image_url = pw.TextField(null=True) 
    attendance = pw.IntegerField(null=True, default=0)
    roles = pw.CharField(null=False)
    # intake_year = 2019 
    # school_name = "SMK BLAH"
    
    # @hybrid_property
    # def full_image_path(self):
    #     from app import app
    #     if self.image_path:
    #         return app.config.get("S3_LOCATION") + self.image_path
    #     else:
    #         return app.config.get("S3_LOCATION") + "blank-profile-picture.png"

    def validate(self):
        # Email should be unique
        existing_user_email = User.get_or_none(User.email==self.email)
        if existing_user_email:
            self.errors.append(f"This email {self.email} already exists!")

        # Name should be unique
        existing_user_full_name = User.get_or_none(User.full_name==self.full_name)
        if existing_user_full_name:
            self.errors.append(f"This name {self.full_name} has already existed!")

        # identity card should be longer than 16 characters
        existing_user_identity_card = User.get_or_none(User.identity_card==self.identity_card)
        if self.identity_card:
            if existing_user_identity_card:
                self.errors.append(f"The IC number {self.identity_card} has already existed!")
            # if self.identity_card:
            #     if len(self.identity_card) != 12:
            #         self.errors.append("NRIC input has to be 12 figures")

        # Password should be longer than 6 characters
        if self.password:
            if len(self.password) <= 6:
                self.errors.append("Password is less than 6 characters")
            # Password should have both uppercase and lowercase characters
            # Password should have at least one special character (REGEX comes in handy here)
            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[\[ \] \* \$ \% \^ \& \# \a]", self.password)

            if has_lower and has_upper and has_special:
                self.password_hash = generate_password_hash(self.password)
            else:
                self.errors.append("Password either does not have upper, lower or special characters!")