from app import app
from .util.assets import bundles
from flask_assets import Environment, Bundle
from flask import render_template
from tutory_web.blueprints.users.views import users_blueprint
from tutory_web.blueprints.sessions.views import sessions_blueprint

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    return render_template('home.html')