from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.exam import Exam
from models.material import Material

exams_api_blueprint = Blueprint('exams_api',
                                __name__,
                                template_folder='templates')

@exams_api_blueprint.route('/', methods=['GET'])
@jwt_required
def index():
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    if user:
        response = []
        for i in Exam:
            response.append({
                "exam.id": i.id,
                "classroom": i.material.classroom_id,
                "staff": i.staff.id,
                "staff": i.staff.full_name,
                "topic": i.material.topic,
                "name": i.material.name,
                "link_url": i.material.link_url
            })
    return jsonify(response)


@exams_api_blueprint.route('/create', methods=['POST'])
@jwt_required
def create():
    params = request.json
    staff = User.get_or_none(User.identity_card == get_jwt_identity())
    #creating a new exam in material database
    new_material = Material(classroom=params.get("classroom_id"), staff=staff.id, topic=params.get("topic"), name=params.get("name"), link_url=params.get("link_url"))
    if staff.roles == "staff":
        if new_material.save():
            new_exam = Exam(material=new_material, staff=staff.id)
            if new_exam.save():
                response = {
                    "Message": "Successfully saved",
                    "Status": "Success",
                    "material.id": new_material.id,
                    "classroom": new_material.classroom_id,
                    "subject": new_material.classroom.subject.name,               
                    "exam.id": new_exam.id,
                    "staff": new_material.staff.id,
                    "staff": new_material.staff.full_name,
                    "topic": new_material.topic,
                    "name": new_material.name,
                    "link_url": new_material.link_url
                }
            else:
                response = {
                    "Message": "Unable to save into Exam",
                    "Status": "Failed",
                }
        else:
            response = {
                "Message": "Unable to save into Material",
                "Status": "Failed",
            }
    else: 
        response = { 
            "Message":"You are not allow to perform this action!"
            }
    return jsonify(response)
    
@exams_api_blueprint.route('/<id>/show', methods=['GET'])
@jwt_required
def show(id):
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    exam = Exam.get_or_none(Exam.id == id)
    if user:
        if exam.id == int(id):
            response = []
            response.append({
                "exam.id": exam.id,
                "classroom": exam.material.classroom_id,
                "staff": exam.staff.id,
                "staff": exam.staff.full_name,
                "topic": exam.material.topic,
                "name": exam.material.name,
                "link_url": exam.material.link_url
            })
    return jsonify(response)

@exams_api_blueprint.route('/<id>/update', methods=['POST'])
@jwt_required
def update(id):   
    staff = User.get_or_none(User.identity_card == get_jwt_identity())
    if staff.roles == "staff":
        params = request.json
        exam = Exam.get_or_none(Exam.id == id)
        material = Material.get_or_none(Material.id == exam.material_id)

        material.classroom = params.get("classroom_id")
        material.topic = params.get("topic")
        material.name = params.get("name")
        material.link_url = params.get("link_url")
        if material.save():
            exam.staff = params.get("staff_id")
            if exam.save():
                response = {
                        "Message": "Successfully saved",
                        "Status": "Success",
                        "material.id": material.id,
                        "classroom": material.classroom_id,
                        "subject": material.classroom.subject.name,               
                        "exam.id": exam.id,
                        "staff": material.staff.id,
                        "staff": material.staff.full_name,
                        "topic": material.topic,
                        "name": material.name,
                        "link_url": material.link_url
                }
            else:
                response = {
                    "Message": "Unable to update exam's data",
                    "Status": "Failed",
                }
        else:
            response = {
                "Message": "Unable to update material's data",
                "Status": "Failed",
            }
    else: 
        response = { 
            "Message":"You are not allow to perform this action!"
            }
    return jsonify(response)

@exams_api_blueprint.route('/delete', methods=['DELETE'])
@jwt_required
def destroy():
    params = request.json
    staff = User.get_or_none(User.identity_card == get_jwt_identity())
    # Deleting an existing data from Material table
    material_id = params.get("id")
    
    if staff.roles == "staff":
        material = Material.get_or_none(Material.id == material_id)
        # Don't need to delete exam table as it's cascade
        if material.delete_instance():
            response = {
                "Message": "Post deleted",
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
    return jsonify(response)