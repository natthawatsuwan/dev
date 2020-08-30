#from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, validators, ValidationError

from flask_wtf import Form, FlaskForm
from wtforms.fields import StringField,PasswordField,SubmitField

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')