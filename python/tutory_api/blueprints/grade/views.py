from flask import Blueprint, render_template, url_for, redirect, request, flash,session, jsonify
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.subject import Subject
from models.grade import Grade

grade_api_blueprint = Blueprint('grade_api',
                            __name__,
                            template_folder='templates')


@grade_api_blueprint.route('/show', methods=['GET'])
@jwt_required
def show():
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    check_user = Grade.get_or_none(Grade.student == user.id)
    if user:
        if check_user or user.roles == "staff":
            grade_list = []
            for grades in Grade:
                grade_list.append({
                    "full_name": grades.student.full_name,
                    "identity_card": grades.student.identity_card,
                    "subject_name": grades.subject.name,
                    "grade": grades.grade
                })
    return jsonify(grade_list)


@grade_api_blueprint.route('/new_grade', methods=['POST'])
@jwt_required
def create():
    user = get_jwt_identity
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    new_grade = Grade(student_id=params.get("student_id"), subject_id=params.get("subject_id"), grade=params.get("grade"), year=params.get("year"))

    if user.roles == "staff":
        if new_grade.save():
            response = []
            for grade in Grade.select():
                response.append({
                    "message": "Grade successfully updated",
                    "status": "Success",
                    "post_id": grade.subject_id,
                    "staff_name": grade.grade,
                    "title": grade.year,
                    "post": grade.student_id
                })
        else:
            response = {
                "error": new_grade.errors,
                "message": "Update failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)


@grade_api_blueprint.route('/<id>/edit_grade', methods=['POST'])
@jwt_required
def edit(id):
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    edit_grade = Grade.get_or_none(Grade.id == id)

    edit_grade.subject = params.get("subject_id")
    edit_grade.grade = params.get("grade")
    edit_grade.student = params.get("student_id")
    edit_grade.year = params.get("year")


    if user.roles == "staff":
        if edit_grade.save():
            response = {
                "message": "Grade successfully edited",
                "status": "Success",
                "subject_id": edit_grade.subject_id,
                "grade": edit_grade.grade,
                "year": edit_grade.year,
                "student_id": edit_grade.student_id
            }
        else:
            response = {
                "error": edit_grade.errors,
                "message": "Edit failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)


@grade_api_blueprint.route('/delete', methods=['DELETE'])
@jwt_required
def delete():
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    check_grade = params.get("id")

    if user.roles == "staff":
        grade = Grade.get_or_none(Grade.id == check_grade)
        if grade.delete_instance():
                response = {
                    "message": "Grade successfully deleted",
                    "status": "Success",
                    "grade_id_deleted": grade.id
                }
        else:
            response = {
                "message": "Delete failed, pkease try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)