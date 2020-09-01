from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
## API Routes ##
from tutory_api.blueprints.users.views import users_api_blueprint
from tutory_api.blueprints.sessions.views import sessions_api_blueprint
from tutory_api.blueprints.materials.views import materials_api_blueprint
from tutory_api.blueprints.assignments.views import assignments_api_blueprint
from tutory_api.blueprints.exams.views import exams_api_blueprint
from tutory_api.blueprints.answers.views import answers_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/sessions')
app.register_blueprint(materials_api_blueprint, url_prefix='/api/v1/materials')
app.register_blueprint(assignments_api_blueprint, url_prefix='/api/v1/assignments')
app.register_blueprint(exams_api_blueprint, url_prefix='/api/v1/exams')
app.register_blueprint(answers_api_blueprint, url_prefix='/api/v1/answers')