from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/signup', methods=['POST'])
def create():
    params = request.json
    new_user = User(full_name=params.get("full_name"), identity_card=params.get("identity_card"), email=params.get("email"), password=params.get("password"), roles=params.get("roles"))
    if new_user.save():
        token = create_access_token(identity=new_user.identity_card)
        response = {
            "auth_token":token,
            "Message": "Successfully logged in",
            "Status": "Success",
            "user": {
                "id": new_user.id,
                "full_name": new_user.full_name
            }            
        }
    else:
        error_message = []
        for error in new_user.errors:
            error_message.append(error)
        response = {
            "Message": error_message,
            "Status": "Failed"
        }
    return jsonify(response)

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    identity_card = get_jwt_identity()
    user = User.get_or_none(User.identity_card == identity_card)
    return jsonify({
        "id": user.id,
        "full_name": user.full_name,
        "identity_card": user.identity_card,
        "email": user.email
    })