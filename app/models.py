from app import app
from flask import Flask, render_template,session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app.config["SQLALCHEMY_DATABASE_URI"] ='postgresql+psycopg2://postgres:postgres@localhost/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

class comment(db.Model):
   idc = db.Column(db.Integer, primary_key=True)
   author = db.Column(db.String(20))
   quote = db.Column(db.String(2000))
   
   
   
class users(db.Model):
    __tablename__ = "users"
    idu = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    hashed_pswd = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def __init__(self,username,hashed_pswd,email ):
        self.username = username
        self.hashed_pswd = hashed_pswd
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' %(self.username)

class loginuser(db.Model):
    
    idu = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    hashed_pswd = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def __init__(self,username,hashed_pswd):
        self.username = username
        self.hashed_pswd = hashed_pswd


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' %(self.username)
	
	
