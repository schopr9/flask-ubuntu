"""
models for user and group
"""
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test4.db'
db = SQLAlchemy(app)


class CRUD():
    """helper crud operation for database"""
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

relationship_table = db.Table('relationship_table',

                              db.Column('user_id', db.Integer, db.ForeignKey(
                                  'user.id'), nullable=False),
                              db.Column('group_id', db.Integer, db.ForeignKey(
                                  'group.id'), nullable=False),
                              db.PrimaryKeyConstraint('user_id', 'group_id'))


class User(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    groups = db.relationship('Group',
                             backref=db.backref('users', lazy= 'dynamic'), secondary=relationship_table)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=not_blank)
    email = fields.Email(validate=not_blank)    
    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/user/"            
        else:
            self_link = "/user/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'users'


class Group(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    date_created = db.Column(db.DateTime)


    def __init__(self, name, data_created=None, user_id=None):
        self.name = name
        self.date_created = datetime.utcnow()
        self.user_id = user_id

    def __repr__(self):
        return '<Group %r>' % self.name


class GroupSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=not_blank)
    date_created = fields.DateTime()

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/groups/"
        else:
            self_link = "/groups/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'groups'
