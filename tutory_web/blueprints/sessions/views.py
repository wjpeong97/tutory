from flask import Blueprint, render_template, url_for, redirect, request, flash,session
from flask_login import login_user, logout_user, login_required
from models.user import User
from werkzeug.security import check_password_hash
# from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/login', methods=['POST'])
def login():
    # get identity_card and password from form
    identity_card = request.form.get("identity_card")
    password = request.form.get("password")
    # check whether have this user in database
    user = User.get_or_none(User.identity_card == identity_card)
    # if got user then check password
    if user:
        result = check_password_hash(user.password_hash,password)
        # if password match then login
        if result:
            flash("Password matched", "primary")
            # save user id in browser session
            # session['user_id'] = user.id 
            login_user(user)
            return redirect(url_for('home', full_name=user.full_name))
        # else error message
        else:
            flash("Password Not matched","danger")
            return  render_template("sessions/new.html")
    # else error message
    else:
        flash("User not found.", "danger")
        return  render_template("sessions/new.html")

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    # remove user info from browser session
    logout_user()
    flash("Logout success!","primary")
    return redirect(url_for("home"))

# @sessions_blueprint.route("/google_login")
# def google_login():
#     redirect_uri = url_for('sessions.authorize', _external = True)
#     return oauth.google.authorize_redirect(redirect_uri)

# @sessions_blueprint.route("/authorize/google")
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