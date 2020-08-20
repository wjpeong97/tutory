from app import app
from .util.assets import bundles
from flask_assets import Environment, Bundle
from flask import render_template
from tutory_web.blueprints.students.views import students_blueprint
from tutory_web.blueprints.staffs.views import staffs_blueprint
# from models.student import Student
# from models.staff import Staff

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(students_blueprint, url_prefix="/students")
app.register_blueprint(staffs_blueprint, url_prefix="/staffs")

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    # students = Student.select()
    # staffs = Staff.select()
    return render_template('home.html')