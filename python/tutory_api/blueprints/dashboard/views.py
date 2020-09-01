from flask import Blueprint, render_template, url_for, redirect, request, flash,session, jsonify
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.announcement import Announcement
from models.activities import Activities

dashboard_api_blueprint = Blueprint('dashboard_api',
                             __name__,
                             template_folder='templates')


@dashboard_api_blueprint.route('/announcement/', methods=['GET'])
@jwt_required
def home_announcement():
    username = get_jwt_identity()
    user = User.get_or_none(User.identity_card == username)

    if user:
        result = []
        for announcement in Announcement.select():
            result.append({
                    "post_id": announcement.id,
                    "staff_name": announcement.full_name,
                    "title": announcement.title,
                    "post": announcement.post
            })
        return jsonify(result)

@dashboard_api_blueprint.route('/activities/', methods=['GET'])
@jwt_required
def home_activities():
    username = get_jwt_identity()
    user = User.get_or_none(User.identity_card == username)

    if user:
        result = []
        for activity in Activities.select():
            result.append({
                    "post_id": activity.id,
                    "staff_name": activity.full_name,
                    "title": activity.title,
                    "post": activity.post
            })
        return jsonify(result)


@dashboard_api_blueprint.route('/announcement/update', methods=['POST'])
@jwt_required
def new_announcement():
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    new_announcements = Announcement(full_name=params.get("full_name"), identity_card=params.get("identity_card"), title=params.get("title"),post=params.get("post"))

    if user.roles == "staff":
        if new_announcements.save():
            response = []
            for announcement in Announcement.select():
                response.append({
                    "message": "New announcement successfully updated",
                    "status": "Success",
                    "post_id": announcement.id,
                    "staff_name": announcement.full_name,
                    "title": announcement.title,
                    "post": announcement.post
                })
        else:
            response = {
                "message": "Update failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)


@dashboard_api_blueprint.route('/activities/update', methods=['POST'])
@jwt_required
def new_activity():
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    new_activity = Activities(full_name=params.get("full_name"), identity_card=params.get("identity_card"), title=params.get("title"),post=params.get("post"))

    if user.roles == "staff":
        if new_activity.save():
            response = []
            for activity in Activities.select():
                response.append({
                    "message": "New activity successfully updated",
                    "status": "Success",
                    "post_id": activity.id,
                    "staff_name": activity.full_name,
                    "title": activity.title,
                    "post": activity.post
                })
        else:
            response = {
                "message": "Update failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)


@dashboard_api_blueprint.route('/announcement/edit', methods=['POST'])
@jwt_required
def edit_announcement_post():
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    edit_post_announcement = Announcement(id=params.get("id"), title=params.get("title"),post=params.get("post"))

    if user.roles == "staff":
        if edit_post_announcement.save():
            for announcement in Announcement.select():
                response = {
                    "message": "Announcement successfully edited",
                    "status": "Success",
                    "post_id": announcement.id,
                    "staff_name": announcement.full_name,
                    "title": announcement.title,
                    "post": announcement.post
                    }
        else:
            response = {
                "message": "Edit failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)


@dashboard_api_blueprint.route('/activities/edit', methods=['POST'])
@jwt_required
def edit_activity_post():
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    edit_post_activity = Activities(id=params.get("id"), title=params.get("title"),post=params.get("post"))

    if user.roles == "staff":
        if edit_post_activity.save():
            for activity in Activities.select():
                response = {
                    "message": "Activity successfully edited",
                    "status": "Success",
                    "post_id": activity.id,
                    "staff_name": activity.full_name,
                    "title": activity.title,
                    "post": activity.post
                    }
        else:
            response = {
                "message": "Edit failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)


@dashboard_api_blueprint.route('/announcement/delete', methods=['DELETE'])
@jwt_required
def delete_announcement():
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    delete_post_announcement = Announcement.get_by_id(params.get("id"))

    if user.roles == "staff":
        if delete_post_announcement.delete_instance():
            for announcement in Announcement.select():
                response = {
                    "message": "Announcement successfully deleted",
                    "status": "Success",
                    "post_id_deleted": delete_post_announcement.id
                }
        else:
            response = {
                "message": "Delete failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)


@dashboard_api_blueprint.route('/activity/delete', methods=['DELETE'])
@jwt_required
def delete_activity():
    params = request.json
    user = User.get_or_none(User.identity_card == get_jwt_identity())
    delete_post_activity = Activities.get_by_id(params.get("id"))

    if user.roles == "staff":
        if delete_post_activity.delete_instance():
            for activity in Activities.select():
                response = {
                    "message": "Activity successfully deleted",
                    "status": "Success",
                    "post_id_deleted": delete_post_activity.id
                }
        else:
            response = {
                "message": "Delete failed, please try again",
                "status": "Failed"
            }
    else:
        response = {"message": "You are not allowed to perform this action!"}
    return jsonify(response)