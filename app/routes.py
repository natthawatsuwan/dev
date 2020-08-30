from app import app
from flask import Flask, render_template,session, redirect, url_for, request,g
from app import connect
import requests
#from app import insert
#from app import view
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, String, Integer
from .models import comment,users,loginuser  #class models import
import hashlib
import os
#from flask_wtf import FlaskForm
from flask import flash
from flask_login import LoginManager,current_user, UserMixin,login_user,logout_user
from .form import LoginForm
#from wtforms import StringField, PasswordField, SubmitField
app.config["SQLALCHEMY_DATABASE_URI"] ='postgresql+psycopg2://postgres:postgres@localhost/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)
import hashlib 

#login config
login = LoginManager(app)
login.init_app(app)

import subprocess

def get_session_user():
    res = subprocess.check_output(["WMIC", "ComputerSystem", "GET", "UserName"],
                                  universal_newlines=True)
    _, username = res.strip().rsplit("\n", 1)
    return username.rsplit("\\", 1)

#usersx=[]#test session user no db
#usersx.append(User(id=1,username='Ant',password='Cat'))
#usersx.append(User(id=2,username='Bat',password='pass'))

#app = Flask(__name__)
app.secret_key ='mysecretdata'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
  return render_template('index.html')
  
@login.user_loader
def load_user(id):
 return users.query.get(0)

@app.before_request
def before_request():
 g.user = None
 if'user'in session:
  g.user = session['user']

@app.route('/protected')
def protected():
  if g.user:
   return redirect(url_for('profile'))
   #render_template('profile.html',user=session['user'])

@app.route('/dropsession')
def dropsession():
 session.pop('user',None)
 return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    hashed_pswd=hashlib.md5(password.encode('utf-8')).hexdigest()
    authen = users.query.filter_by(username = username).first()
    if authen is None:
     render_template('login.html',status='ไม่พบไอดี กรุณาสมัครสมาชิก')
    if (username==authen.username and hashed_pswd==authen.hashed_pswd):
        user = loginuser(username,hashed_pswd)
        user.id = username
        login_user(user)
        session['user']= request.form['username']
        return redirect(url_for('protected'))

    return render_template('login.html',status='ไอดี หรือ รหัสผ่าน ไม่ถูกต้อง')
	


@app.route("/logout", methods=['GET'])
def logout():

    # Logout user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))
	
@app.route('/profile')
def profile():
 if not session.get("user") is None:
        return render_template("profile.html",name=session['user'])
 else:
        print("No username found in session")
        return redirect(url_for("login"))
	
@app.route('/registfrom')
def registfrom():
  return  render_template('register.html')

  
@app.route('/register',methods=['POST'])#process register
def register():
  username = request.form['username']
  password = request.form['password']
  email = request.form['email']
  hashed_pswd=hashlib.md5(password.encode('utf-8')).hexdigest() #MD5
  #salt = os.urandom(32)                #SHA-256
  #hashed_pswd = hashlib.pbkdf2_hmac(
    #'sha256', # The hash digest algorithm for HMAC
    #password.encode('utf-8'), # Convert the password to bytes
    #salt, # Provide the salt
    #100000, # It is recommended to use at least 100,000 iterations of SHA-256 
    #dklen=128 )

  regist = users(username=username,hashed_pswd=hashed_pswd,email=email)
  db.session.add(regist)
  db.session.commit()
  return render_template('index.html')

@app.route('/update')
def update():
  userss = users.query.with_entities(users.username,users.email).all() #nopass
  return  render_template('update.html',result=userss)

  
  
@app.route('/process',methods=['POST'])  #comment support
def process():
  authors = request.form['author']
  quotes = request.form['quote']
  quoutedata =comment(author=authors,quote=quotes)
  db.session.add(quoutedata)
  db.session.commit()
  result = comment.query.all()
  return render_template('support.html',result=result)

@app.route('/search',methods=['GET','POST'])
def search():
  authors = request.form['search']
  result = comment.query.filter_by(author = authors).all()
  return render_template('support.html',result=result,)  
  
@app.route('/support')
def support():
  result = comment.query.all()
  return render_template('support.html',result=result)