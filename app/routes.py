from app import app
from flask import Flask, render_template,session, redirect, url_for, request
from app import connect
#from app import insert
#from app import view
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, String, Integer

app.config["SQLALCHEMY_DATABASE_URI"] ='postgresql+psycopg2://postgres:postgres@localhost/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

class comment(db.Model):
   idc = db.Column(db.Integer, primary_key=True)
   author = db.column(db.String(20))
   
   quote = db.column(db.String(2000))

   

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Boom')
def myDave():
    return 'Hello World - From Boom'

@app.route('/home')
def home():
  return render_template('index2.html',name="boom")

@app.route('/person')
def person():
  return 'Hello World - From Person'

@app.route('/login', methods=['GET', 'POST'])
def login():
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
  
@app.route('/connect')
def connect():
  return  'PostgreSQL connection is closed'

@app.route('/register')  
def register():
  return  '''
        <form method="post">
		         
            <p>username:      <input type=text name=username>
			<p>password:      <input type=password name=password>
			<p>auth-password: <input type=password name=auth-password>
			<p>e-mail:        <input type=text name=email>
            <p><input type=submit value=agree>
        </form>
    ''' 
  
@app.route('/quotes')
def quotes():
  return render_template('quotes.html')
  
  
@app.route('/process',methods=['POST'])
def process():
  author = request.form['author']
  quote = request.form['quote']
  
  #quoutedata =comment(author=author,quote=quote)
  #db.session.add(quotedata)
  #db.session.commit()
  
  return redirect(url_for('support.html'))
  
  
  
@app.route('/support')
def support():
  result = comment.query.all()
  fruits = ["apple","grapes","berries","oranges"]
  return render_template('support.html',quotes="boom",fruits=fruits,result=result)