from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.assignment import Assignment

assignments_api_blueprint = Blueprint('assignments_api',
                                __name__,
                                template_folder='templates')

@assignments_api_blueprint.route('/', methods=['GET'])
@jwt_required
def index():
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    if user:
        response = []
        for i in Assignment:
            response.append({
                "assignment.id": i.id,
                "classroom": i.classroom_id,
                "subject": i.classroom.subject.name,
                "student": i.student.full_name,
                "topic": i.topic,
                "name": i.name,
                "link_url": i.link_url
            })
    return jsonify(response)


@assignments_api_blueprint.route('/create', methods=['POST'])
@jwt_required
def create():
    params = request.json
    student = User.get_or_none(User.identity_card == get_jwt_identity())
    new_assignment = Assignment(classroom=params.get("classroom_id"), student=student.id, topic=params.get("topic"), name=params.get("name"), link_url=params.get("link_url"))
    if student.roles == "student":
        if new_assignment.save():
            response = {
                "Message": "Successfully saved",
                "Status": "Success",
                "assignment.id": new_assignment.id,
                "classroom": new_assignment.classroom_id,
                "subject": new_assignment.classroom.subject.name,
                "topic": new_assignment.topic,
                "name": new_assignment.name,
                "link_url": new_assignment.link_url
            }
        else:
            response = {
                "Message": "Action unsuccessful",
                "Status": "Failed",   
            }
        return jsonify(response)
    else: 
        response = { 
            "Message":"You are not allow to perform this action!"
            }
    return jsonify(response)
    
@assignments_api_blueprint.route('/<id>/show', methods=['GET'])
@jwt_required
def show(id):
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    assignment = Assignment.get_or_none(Assignment.id == id)
    if user:
        if assignment.id == int(id):
            response = []
            response.append({
                "assignment.id": assignment.id,
                "classroom": assignment.classroom_id,
                "subject": assignment.classroom.subject.name,
                "student": assignment.student.full_name,
                "topic": assignment.topic,
                "name": assignment.name,
                "link_url": assignment.link_url
            })
    return jsonify(response)

@assignments_api_blueprint.route('/<id>/update', methods=['POST'])
@jwt_required
def update(id):   
    student = User.get_or_none(User.identity_card == get_jwt_identity())
    if student.roles == "student":
        params = request.json
        assignment = Assignment.get_or_none(Assignment.id == id)

        assignment.student = student.id
        assignment.classroom = params.get("classroom_id")
        assignment.topic = params.get("topic")
        assignment.name = params.get("name")
        assignment.link_url = params.get("link_url")
        if assignment.save():
            response = {
                "Message": "Successfully edited",
                "Status": "Success",
                "assignment.id": assignment.id,
                "classroom": assignment.classroom_id,
                "subject": assignment.classroom.subject.name,
                "topic": assignment.topic,
                "name": assignment.name,
                "link_url": assignment.link_url
            }
        else:
            response = {
                "Message": "Action unsuccessful",
                "Status": "Failed",   
            }
    else: 
        response = { 
            "Message":"You are not allow to perform this action!"
            }
    return jsonify(response)

@assignments_api_blueprint.route('/delete', methods=['DELETE'])
@jwt_required
def destroy():
    params = request.json
    # to get current user
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    assignment_id = params.get("id")

    if user:
        assignment = Assignment.get_or_none(Assignment.id == assignment_id)
        # to check only the student who submitted will be only one who can delete + any staffs can delete it
        if assignment.student.id == user.id or user.roles == "staff":
            if assignment.delete_instance():
                response = {
                    "Message": "Assignment deleted",
                    "Status": "Success"
                }
            else:
                response = {
                    "Message": "Action unsuccessful",
                    "Status": "Failed"
                }
        else: 
            response = { 
                "Message":"You are not allow to perform this action!"
                }
    else: 
        response = { 
            "Message":"You are not allow to perform this action!"
            }
    return jsonify(response)