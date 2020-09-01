from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.material import Material

materials_api_blueprint = Blueprint('materials_api',
                                __name__,
                                template_folder='templates')

@materials_api_blueprint.route('/', methods=['GET'])
@jwt_required
def index():
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    if user:
        response = []
        for i in Material:
            response.append({
                "material.id": i.id,
                "classroom": i.classroom_id,
                "subject": i.classroom.subject.name,
                "staff": i.staff.full_name,
                "topic": i.topic,
                "name": i.name,
                "link_url": i.link_url
            })
    return jsonify(response)


@materials_api_blueprint.route('/create', methods=['POST'])
@jwt_required
def create():
    params = request.json
    staff = User.get_or_none(User.identity_card == get_jwt_identity())
    new_material = Material(classroom=params.get("classroom_id"), staff=staff.id, topic=params.get("topic"), name=params.get("name"), link_url=params.get("link_url"))
    if staff.roles == "staff":
        if new_material.save():
            response = {
                "Message": "Successfully saved",
                "Status": "Success",
                "material.id": new_material.id,
                "classroom": new_material.classroom_id,
                "subject": new_material.classroom.subject.name,                
                "topic": new_material.topic,
                "name": new_material.name,
                "link_url": new_material.link_url
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
    
@materials_api_blueprint.route('/<id>/show', methods=['GET'])
@jwt_required
def show(id):
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    material = Material.get_or_none(Material.id == id)
    if user:
        if material.id == int(id):
            response = []
            response.append({
                "material.id": material.id,
                "classroom": material.classroom_id,
                "subject": material.classroom.subject.name,
                "staff": material.staff.full_name,
                "topic": material.topic,
                "name": material.name,
                "link_url": material.link_url
            })
    return jsonify(response)

@materials_api_blueprint.route('/<id>/update', methods=['POST'])
@jwt_required
def update(id):   
    staff = User.get_or_none(User.identity_card == get_jwt_identity())
    if staff.roles == "staff":
        params = request.json
        material = Material.get_or_none(Material.id == id)

        material.classroom = params.get("classroom_id")
        material.topic = params.get("topic")
        material.name = params.get("name")
        material.link_url = params.get("link_url")
        if material.save():
            response = {
                "Message": "Successfully edited",
                "Status": "Success",
                "material.id": material.id,
                "classroom": material.classroom_id,
                "subject": material.classroom.subject.name,
                "topic": material.topic,
                "name": material.name,
                "link_url": material.link_url
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

@materials_api_blueprint.route('/delete', methods=['DELETE'])
@jwt_required
def destroy():
    params = request.json
    staff = User.get_or_none(User.identity_card == get_jwt_identity())
    material_id = params.get("id")
    if staff.roles == "staff":
        material = Material.get_or_none(Material.id == material_id)
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