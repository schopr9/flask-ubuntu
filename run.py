"""
author saurabh
This module will serve as rest api for model user and group
"""
import os
from flask import Flask, jsonify, request, make_response, Response, Request
from model.models import db, User, Group, CRUD, UserSchema, GroupSchema, app
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError


class MyResponse(Response):
    default_mimetype = 'application/json'


def request_wants_json():
    return request.content_type == 'application/json'

app.response_class = MyResponse
user_schema = UserSchema()
group_schema = GroupSchema()


@app.before_request
def before_request():
    """check request content type else return error"""
    if request_wants_json():
        pass
    else:
        resp = jsonify({"error": "request should be json"})
        resp.status_code = 400
        return resp


@app.route('/users', methods=['GET'])
def users():
    """list all the users"""
    users = User.query.order_by(User.username)
    results = user_schema.dump(users, many=True).data
    return jsonify({'users': results})


@app.route('/user/new', methods=['POST'])
def user_new():
    """create new user"""
    raw_dict = request.get_json(force=True)
    try:
        user_schema.validate(raw_dict)
        user_dict = raw_dict['data']['attributes']
        user = User(user_dict['username'], user_dict['email'])
        user.add(user)
        query = User.query.filter_by(email=user_dict['email']).first()
        print query
        results = user_schema.dump(query).data
        print results
        return jsonify({"id": query.id})

    except ValidationError as err:

        resp = jsonify({"error": err.messages})
        resp.status_code = 403
        return resp

    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 403
        return resp


@app.route('/user/<id>', methods=['GET'])
def user_get(id):
    """retreive single user"""
    user = User.query.get_or_404(id)
    results = user_schema.dump(user).data
    return jsonify({'users': results})


@app.route('/user/<id>', methods=['DELETE'])
def user_delete(id):
    """delete specific user"""
    user = User.query.get_or_404(id)
    try:
        delete = user.delete(user)
        response = make_response()
        response.status_code = 204
        return response

    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 401
        return resp


@app.route('/user/<id>', methods=['PATCH'])
def user_update(id):
    """update specific user"""
    user = User.query.get_or_404(id)
    raw_dict = request.get_json(force=True)

    try:
        user_schema.validate(raw_dict)
        user_dict = raw_dict['data']['attributes']
        for key, value in user_dict.items():

            setattr(user, key, value)

        user.update()
        results = user_schema.dump(user).data
        return jsonify(results)

    except ValidationError as err:
        resp = jsonify({"error": err.messages})
        resp.status_code = 401
        return resp

    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 401
        return resp


@app.route('/groups', methods=['GET'])
def groups():
    """list all groups"""
    groups = Group.query.order_by(Group.name)
    results = group_schema.dump(groups, many=True).data
    return jsonify({'groups': results})


@app.route('/group/<id>', methods=['GET'])
def group_get(id):
    """retreive specific group"""
    group = Group.query.get(id)
    results = group_schema.dump(group).data
    return jsonify({'group': results})


@app.route('/group/new', methods=['POST'])
def group_new():
    """create group"""
    raw_dict = request.get_json(force=True)
    try:
        group_schema.validate(raw_dict)
        group_dict = raw_dict['data']['attributes']
        group = Group(group_dict['name'])
        group.add(group)
        query = Group.query.filter_by(name=group_dict['name']).first()
        results = group_schema.dump(query).data
        print results
        return jsonify({"id": query.id})

    except ValidationError as err:

        resp = jsonify({"error": err.messages})
        resp.status_code = 403
        return resp

    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 403
        return resp


@app.route('/group/<id>', methods=['PATCH'])
def group_update(id):
    """update group"""
    group = Group.query.get_or_404(id)
    raw_dict = request.get_json(force=True)

    try:
        group_schema.validate(raw_dict)
        group_dict = raw_dict['data']['attributes']
        for key, value in group_dict.items():

            setattr(group, key, value)

        group.update()
        results = group_schema.dump(group).data
        return jsonify(results)

    except ValidationError as err:
        resp = jsonify({"error": err.messages})
        resp.status_code = 401
        return resp

    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 401
        return resp


@app.route('/user/<id>/groups', methods=['POST'])
def user_add_groups(id):
    """ user can be added to multiple groups"""
    user = User.query.get_or_404(id)
    raw_dict = request.get_json(force=True)

    for group_id in raw_dict['groups']:
        group = Group.query.get(group_id)
        if group:
            user.groups.append(group)

    if user:
        user.update()
        results = user_schema.dump(user).data
        return jsonify(results)
    else:
        resp = jsonify({"error": "group or user not found"})
        resp.status_code = 404
        return resp


@app.route('/user/<id>/groups', methods=['DELETE'])
def user_remove_groups(id):
    """user can be removed from multiple groups"""
    user = User.query.get_or_404(id)
    raw_dict = request.get_json(force=True)

    for group_id in raw_dict['groups']:
        group = Group.query.get(group_id)
        if group:
            user.groups.remove(group)

    if user:
        user.update()
        results = user_schema.dump(user).data
        return jsonify(results)
    else:
        resp = jsonify({"error": "group or user not found"})
        resp.status_code = 404
        return resp

@app.route('/user/<id>/groups', methods=['GET'])
def user_groups(id):
    """list groups for a user"""
    user = User.query.get(id)

    if user:
        user_groups = user.groups
        results = []
        for obj in user_groups:
            results.append(obj.name)
        return jsonify({"groups": results})
    else:
        resp = jsonify({"error": "user not found"})
        resp.status_code = 404
        return resp


@app.route('/group/<id>/users', methods=['GET'])
def group_users(id):
    """list users for a group"""
    group = Group.query.get(id)

    if group:
        group_users = group.users
        results = []
        for obj in group_users:
            results.append(obj.username)
        return jsonify({"users": results})
    else:
        resp = jsonify({"error": "group not found"})
        resp.status_code = 404
        return resp

app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
