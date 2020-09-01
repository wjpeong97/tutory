from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.answer import Answer
from models.exam import Exam
from tutory_api.util.helpers import upload_file_to_s3
import tempfile

answers_api_blueprint = Blueprint('answers_api',
                                __name__,
                                template_folder='templates')

@answers_api_blueprint.route('/', methods=['GET'])
@jwt_required
def index():
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    if user:
        response = []
        for i in Answer:
            response.append({
                "exam.id": i.exam_id,
                "material.id": i.exam.material_id,
                "material.name": i.exam.material.name,
                "subject.id": i.exam.material.classroom.subject.id,
                "subject.name": i.exam.material.classroom.subject.name,
                "staff.id": i.exam.staff_id,
                "staff.name": i.exam.staff.full_name,
                "student.id": i.student_id,
                "student.name": i.student.full_name,
                "submission": i.full_file_url
            })
    return jsonify(response)


@answers_api_blueprint.route('/create', methods=['POST'])
@jwt_required
def create():
    student = User.get_or_none(User.identity_card == get_jwt_identity())
    params = request.json
    new_submission = Answer(exam_id=params.get("exam_id"), student_id=student.id, submission=params.get("submission"))

    if student.roles == "student":
        # check if there's existing data in Answer's table
        check_table = Answer.get_or_none((Answer.exam_id == new_submission.exam.id) & (Answer.student_id == new_submission.student.id))
        if not check_table:
            # putting the txt from submission to a tempfile
            temp = tempfile.TemporaryFile()
            temp.write(new_submission.submission.encode("utf-8"))

            # get path from S3
            file_path = upload_file_to_s3(temp, get_jwt_identity(), new_submission.exam)
            
            # save path into the table
            answer = Answer(exam=new_submission.exam, submission=file_path, student=student.id)

            if answer.save():
                response = {
                    "Message": "Successfully saved",
                    "Status": "Success",              
                    "exam.id": answer.exam_id,
                    "material.id": answer.exam.material_id,
                    "material.name": answer.exam.material.name,
                    "subject.id": answer.exam.material.classroom.subject.id,
                    "subject.name": answer.exam.material.classroom.subject.name,
                    "staff.id": answer.exam.staff_id,
                    "staff.name": answer.exam.staff.full_name,
                    "student.id": answer.student_id,
                    "student.name": answer.student.full_name,
                    "submission": answer.full_file_url
                }
            else:
                response = {
                    "Message": "Action unsuccessful",
                    "Status": "Failed",   
                }
        else: 
            response = { 
                "Message":"There is an existing submission!"
                }
    else: 
        response = { 
            "Message":"You are not allow to perform this action!"
            }
    return jsonify(response)
    
@answers_api_blueprint.route('/<id>/show', methods=['GET'])
@jwt_required
def show(id):
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    answer = Answer.get_or_none(Answer.id == id)
    if user:
        if answer.id == int(id):
            response = []
            response.append({
                "exam.id": answer.exam_id,
                "material.id": answer.exam.material_id,
                "material.name": answer.exam.material.name,
                "subject.id": answer.exam.material.classroom.subject.id,
                "subject.name": answer.exam.material.classroom.subject.name,
                "staff.id": answer.exam.staff_id,
                "staff.name": answer.exam.staff.full_name,
                "student.id": answer.student_id,
                "student.name": answer.student.full_name,
                "submission": answer.full_file_url
            })
    return jsonify(response)

## cannot edit the submission once submitted
# @answers_api_blueprint.route('/<id>/update', methods=['POST'])
# @jwt_required
# def update(id):   
#     student = User.get_or_none(User.identity_card == get_jwt_identity())
#     if student.roles == "student":
#         params = request.json
#         answer = Answer.get_or_none(Answer.id == id)

#         answer.exam = params.get("exam_id")
#         answer.student = student.id
#         answer.submission = params.get("submission")
        
#         # putting the txt from submission to a tempfile
#         temp = tempfile.TemporaryFile()
#         temp.write(answer.submission.encode("utf-8"))

#         # get path from S3
#         file_path = upload_file_to_s3(temp, get_jwt_identity())
        
#         # save path into the table
#         answer = Answer(exam=answer.exam, submission=file_path, student=student.id)

#         if answer.save():
#             response = {
#                 "Message": "Successfully edited",
#                 "Status": "Success",
#                 "exam.id": answer.exam_id,
#                 "material.id": answer.exam.material_id,
#                 "material.name": answer.exam.material.name,
#                 "subject.id": answer.exam.material.classroom.subject.id,
#                 "subject.name": answer.exam.material.classroom.subject.name,
#                 "staff.id": answer.exam.staff_id,
#                 "staff.name": answer.exam.staff.full_name,
#                 "student.id": answer.student_id,
#                 "student.name": answer.student.full_name,
#                 "submission": answer.full_file_url
#             }
#         else:
#             response = {
#                 "Message": "Action unsuccessful",
#                 "Status": "Failed",   
#             }
#     else: 
#         response = { 
#             "Message":"You are not allow to perform this action!"
#             }
#     return jsonify(response)

@answers_api_blueprint.route('/delete', methods=['DELETE'])
@jwt_required
def destroy():
    params = request.json
    # to get current user
    user = User.get_or_none(User.identity_card == get_jwt_identity())    
    answer_id = params.get("id")

    if user: 
        answer = Answer.get_or_none(Answer.id == answer_id)
        ##[DONT NEED] to check only the student who submitted will be only one who can delete + any staffs can delete it
        # if answer.student.id == user.id or user.roles == "staff":

        ## only staff can delete the submission
        if user.roles == "staff":
            if answer.delete_instance():
                response = {
                    "Message": "Submission deleted",
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