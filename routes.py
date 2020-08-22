from app import app
from flask import Flask, render_template

@app.route('/')
def hello_world():
    return 'ไม่มีหน้าที่แสดง'

@app.route('/Boom')
def myDave():
    return 'Hello World - From Boom'

@app.route('/home')
def home():
  return render_template('index.html',name="boom")

@app.route('/about')
def about():
  return render_template('about.html')