from flask import Blueprint, request, jsonify
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
# from instagram_web.util.google_oauth import oauth

sessions_api_blueprint = Blueprint('sessions_api',
                                __name__,
                                template_folder='templates')

@sessions_api_blueprint.route('/login', methods=['POST'])
def login():
    # get identity_card and password from form
    identity_card = request.json.get("identity_card")
    password = request.json.get("password")
    # check whether have this user in database
    user = User.get_or_none(User.identity_card == identity_card)
    # if got user then check password
    if user:
        result = check_password_hash(user.password_hash,password)
        # if password match then login
        if result:
            token = create_access_token(identity=user.identity_card)
            response = {
                "auth_token":token,
                "Message": "Successfully logged in",
                "Status": "Success",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name
                }            
        }
        else:
            response = {
                "Message": "Unsuccessful login",
                "Status": "Failed",
            }
    else:
        response = {
        "Message": "User not found",
        "Status": "Failed",
        }
    return jsonify(response)

# @sessions_api_blueprint.route('/delete', methods=['POST'])
# @login_required
# def destroy():
#     # remove user info from browser session
#     logout_user()
#     flash("Logout success!","primary")
#     return redirect(url_for("home"))

# @sessions_api_blueprint.route("/google_login")
# def google_login():
#     redirect_uri = url_for('sessions.authorize', _external = True)
#     return oauth.google.authorize_redirect(redirect_uri)

# @sessions_api_blueprint.route("/authorize/google")
# def authorize():
#     oauth.google.authorize_access_token()
#     email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
#     user = User.get_or_none(User.email == email)
#     if user:
#         login_user(user)
#         flash("Sign in successfully.", "primary")
#         return redirect(url_for('sessions.show',username=user.username))
#     else:
#         flash("Sign up to continue.", "danger")
#         return redirect(url_for('sessions.new'))