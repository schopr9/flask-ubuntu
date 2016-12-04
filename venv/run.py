import os
from flask import Flask, jsonify, request, make_response, Response
from model.models import db, User, Group, CRUD, UserSchema, GroupSchema, app
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

class MyResponse(Response):
     default_mimetype = 'application/json'

app.response_class = MyResponse
user_schema = UserSchema()
group_schema = GroupSchema()

@app.route('/')
def hello():
    return 'Hello World'


@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    results = user_schema.dump(users, many=True).data
    return jsonify({'users': results})


@app.route('/user/new', methods=['POST'])
def user_new():
    raw_dict = request.get_json(force=True)
    try:
        user_schema.validate(raw_dict)
        user_dict = raw_dict['data']['attributes']
        user = User(user_dict['username'],user_dict['email'])
        user.add(user)            
        query = User.query.filter_by(email= user_dict['email']).first()
        print query
        results = user_schema.dump(query).data    
        print results
        return jsonify({"id" : query.id})
        
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
    user = User.query.get(id)
    results = user_schema.dump(user).data
    return jsonify({'users': results})


@app.route('/user/<id>', methods=['DELETE'])
def user_delete(id):
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
    groups = Group.query.all()
    results = group_schema.dump(groups, many=True).data
    return jsonify({'groups': results})

@app.route('/group/<id>', methods=['GET'])
def group_get(id):
    group = Group.query.get(id)
    results = group_schema.dump(group).data
    return jsonify({'group': results})

@app.route('/group/new', methods=['POST'])
def group_new():
    raw_dict = request.get_json(force=True)
    try:
        group_schema.validate(raw_dict)
        group_dict = raw_dict['data']['attributes']
        group = Group(group_dict['name'])
        group.add(group)            
        query = Group.query.filter_by(name= group_dict['name']).first()
        results = group_schema.dump(query).data    
        print results
        return jsonify({"id" : query.id})
        
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


@app.route('/user/<id>/groups', methods=['GET'])
def user_groups(id):
    user = User.query.get_or_404(id)

    if user:
        user_groups = user.groups.all()
        results = []
        for obj in user_groups:
            results.append(obj.name)
        return jsonify({"groups" :results})
    else:
        return jsonify({"err" : "user not found"})
            
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))