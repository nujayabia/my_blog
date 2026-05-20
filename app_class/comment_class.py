from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length, Optional
from flask_ckeditor import  CKEditorField


class CommentData():
    def __init__(self,form_data):
        self.text = form_data.get('text')
        self.date= form_data.get('date')
        self.user_id= form_data.get('user_id')
        self.post_id= form_data.get('post_id')


class CommentForm(FlaskForm):
    text=CKEditorField("Comment:", validators=([DataRequired('Required!!')]))
    submit = SubmitField('Submit a comment',render_kw={"class":"btn btn-info"})
