from app import app
from flask import render_template
from flask_assets import Environment, Bundle
from .util.assets import bundles
from tutory_web.blueprints.students.views import students_blueprint
from models.student import Student

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(students_blueprint, url_prefix="/students")

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    # students = Student.select()
    return render_template('home.html')