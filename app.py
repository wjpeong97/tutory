import os
import config
from flask import Flask
from models.base_model import db
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from models.student import Student
from models.staff import Staff
  
web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'tutory_web')

app = Flask('TUTORY', root_path=web_dir)
CSRFProtect(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

login_manager = LoginManager()
login_manager.init_app(app) # configure the app for flask-login

login_manager.login_view = "home"   # if user try to access login_required route without sign in, will redirect to `home`
login_manager.login_message = "Please log in before proceeding"
login_manager.login_message_category = "warning"

# This callback is used to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    return Student.get_or_none(Student.id == user_id) or Staff.get_or_none(Staff.id == user_id)

# @login_manager.user_loader
# def load_user(user_id):
#     student = Student.get_or_none(Student.id == user_id)
#     staff = Staff.get_or_none(Staff.id == user_id)
#     if student:
#         return student
#     elif staff:
#         return staff
#     else:
#         return None


@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
