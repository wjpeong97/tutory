from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash
from models.staff import Staff
# from tutory_web.util.helpers import upload_file_to_s3
# from werkzeug import secure_filename

staffs_blueprint = Blueprint('staffs',
                            __name__,
                            template_folder='templates')

@staffs_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('staffs/new.html')

@staffs_blueprint.route('/signup', methods=['POST'])
def create():
    params = request.form
    new_user = Staff(full_name=params.get("full_name"), identity_card=params.get("identity_card"), email=params.get("email"), password=params.get("password"))
    if new_user.save():
        flash("Successfuly Sign Up!", "success")
        login_user(new_user)
        return redirect(url_for("home", full_name=new_user.full_name))
    else:
        for err in new_user.errors:
            flash(err, "danger")
        return redirect(url_for("staffs.new"))

@staffs_blueprint.route('/login', methods=['POST'])
def login():
    # get identity_card and password from form
    identity_card = request.form.get("identity_card")
    password = request.form.get("password")
    # check whether have this user in database
    user = Staff.get_or_none(Staff.identity_card == identity_card)
    # if got user then check password
    if user:
        result = check_password_hash(user.password_hash,password)
        # if password match then login
        if result:
            flash("Password matched", "primary")
            # save user id in browser session
            # session['user_id'] = user.id 
            login_user(user)
            return redirect(url_for('home',full_name=user.full_name))
        # else error message
        else:
            flash("Password Not matched","danger")
            return  render_template("staffs/new.html")
    # else error message
    else:
        flash("Staff not found.", "danger")
        return  render_template("staffs/new.html")

@staffs_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    # remove user info from browser session
    logout_user()
    flash("Logout success!","primary")
    return redirect(url_for("home"))


# @users_blueprint.route('/<username>', methods=["GET"])  # user profile page
# @login_required   # only can access this route after signed in
# def show(username):
#     user = User.get_or_none(User.username == username) # check whether user exist in database
#     if user:
#         return render_template("users/show.html",user=user)
#     else:
#         flash(f"No {username} user found.", "danger" )
#         return redirect(url_for('home'))

# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"

# @users_blueprint.route('/<id>/edit', methods=['GET'])
# @login_required
# def edit(id):
#     user = User.get_or_none(User.id== id)
#     if user:
#         if current_user.id == int(id):
#             return render_template("users/edit.html", user=user)
#         else:
#             flash("Cannot edit users other than yourself!")
#             return redirect(url_for("users.show", username=user.username))
#     else:
#         flash("No such user!")
#         return redirect(url_for("home"))

# @users_blueprint.route('/<id>', methods=['POST'])
# @login_required
# def update(id):
#     user = User.get_or_none(User.id == id)
#     if user:
#         if current_user.id == int(id):
#             params = request.form

#             user.is_private = True if params.get("private") == "on" else False

#             user.username = params.get("username")
#             user.email = params.get("email")

#             password = params.get("password")

#             if len(password) > 0:
#                 user.password = password
            
#             if user.save():
#                 flash("Successfully updated user!")
#                 return redirect(url_for("users.show", username=user.username))
#             else:
#                 flash("Unable to edit!")
#                 for err in user.errors:
#                     flash(err)
#                 return redirect(url_for("users.edit", id=user.id))
#         else:
#             flash("Cannot edit users other than yourself!")
#             return redirect(url_for("users.show", username=user.username))
#     else:
#         flash("No such user!")
#         redirect(url_for("home"))


# @users_blueprint.route('/<id>/upload', methods=['POST'])
# @login_required
# def upload(id):
#     user = User.get_or_none(User.id == id)
#     if user:
#         if current_user.id == int(id):
#             # Upload image
#             if "profile_image" not in request.files:
#                 flash("No file provided!")
#                 return redirect(url_for("users.edit", id=id))

#             file = request.files["profile_image"]

#             file.filename = secure_filename(file.filename)
#             # Get path to image on s3 bucket
#             image_path = upload_file_to_s3(file,user.username )
#             # Update user with image path
#             user.image_path = image_path
#             if user.save():
#                 return redirect(url_for("users.show", username=user.username))
#             else:
#                 flash("Could not upload image. Please try again")
#                 return redirect(url_for("users.edit", id=id))       
#         else:
#             flash("Cannot edit users other than yourself!")
#             return redirect(url_for("users.show", username=user.username))
#     else:
#         flash("No such user!")
#         redirect(url_for("home"))