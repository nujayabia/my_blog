from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField,EmailField,PasswordField
from wtforms.validators import DataRequired, URL, Length
from flask_ckeditor import  CKEditorField


class UserData():
    def __init__(self,form_data):
        self.name = form_data['name']
        self.email = form_data['email']
        self.password = form_data['password']




class UserForm(FlaskForm):
    name=StringField("Name:",validators=([DataRequired('Required!!'),Length(1,250,message="Name must be between 1 and 250 character")]))
    email=EmailField("Email:",validators=([DataRequired('Required!!')]))
    password=PasswordField("Password:",validators=([DataRequired('Required!!'),Length(8,message="Passowrd must be more than or equal to  8 characters")]))
    submit = SubmitField('Submit',render_kw={"class":"btn btn-success"})

class LoginForm(FlaskForm):
    email=EmailField("Email:",validators=([DataRequired('Required!!')]))
    password=PasswordField("Password:",validators=([DataRequired('Required!!'),Length(8,message="Passowrd must be more than or equal to  8 characters")]))
    submit = SubmitField('Submit',render_kw={"class":"btn btn-success"})