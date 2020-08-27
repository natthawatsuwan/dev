from app import app
from flask import Flask, render_template,session, redirect, url_for, request
from app import connect
#from app import insert
#from app import view
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, String, Integer
from .models import comment,users   #class models import
import hashlib
import os
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
  return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  if request.method == 'POST':
   username = request.form['username']
   password = request.form['password']
   
   #user = [x for x in users if x.username==username]   
  return render_template('signin.html',username=username,password= password)
  
@app.route('/logins', methods=['GET', 'POST'])
def logins():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
		         
            <p>username: <input type=text name=username>
			<p>password: <input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''  
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    #form = LoginForm()
    #if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        #login_user(user)

        #flask.flash('Logged in successfully.')

        #next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        #if not is_safe_url(next):
            #return flask.abort(400)

        #return flask.redirect(next or flask.url_for('index'))
    return render_template('signin.html')
	
	
@app.route('/registfrom')
def registfrom():
  return  render_template('register.html')

  
@app.route('/register',methods=['POST'])#process register
def register():
  username = request.form['username']
  password = request.form['password']
  email = request.form['email']
  
  salt = os.urandom(32)
  hashed_pswd = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000, # It is recommended to use at least 100,000 iterations of SHA-256 
    dklen=128 )

  regist =users(username=username,hashed_pswd=hashed_pswd,email=email)
  db.session.add(regist)
  db.session.commit()
  return render_template('index.html')

@app.route('/update')
def update():
  result = users.query.all()
  return  render_template('update.html',result=result)

  
  
@app.route('/process',methods=['POST'])  #comment support
def process():
  authors = request.form['author']
  quotes = request.form['quote']
  quoutedata =comment(author=authors,quote=quotes)
  db.session.add(quoutedata)
  db.session.commit()
  result = comment.query.all()
  return render_template('support.html',result=result)
  
  
@app.route('/support')
def support():
  result = comment.query.all()
  return render_template('support.html',result=result)