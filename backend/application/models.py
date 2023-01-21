from enum import unique
from sqlalchemy.orm import backref
from .database import db
from flask_security import UserMixin




class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(255))
    # active = db.Column(db.Boolean())
    deck = db.relationship(
        "List", backref='user')
    
    # def __init__(self, username, active=0):
    #     self.username=username
    #     self.active=active 

    # def is_active(self):
    #     return True

    # def is_authenticated(self):
    #     return True

    # def is_anonymous(self):
    #     return False


    # def get_id(self):
    #     return self.user_id
    
    # def get_username(self):
    #     return self.username



class List(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    card = db.relationship("Card", backref='list')


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)
    completed_time = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime)
    completed = db.Column(db.Integer,default=0)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    deadline_days=db.Column(db.Integer,nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'list.id'), primary_key=True, nullable=False)
  
    


