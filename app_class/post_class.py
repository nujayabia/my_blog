from flask_wtf import FlaskForm
from markupsafe import Markup
from sqlalchemy import Nullable
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length, Optional
from flask_ckeditor import  CKEditorField


class PostData():
    def __init__(self,form_data):
        self.title = form_data.get('title')
        self.subtitle = form_data.get('subtitle')
        self.date = form_data.get('date')
        self.body = form_data.get('body')
        self.author = form_data.get('author')
        self.img_url = form_data.get('img_url')
        self.added_by_id = form_data.get('added_by_id')
        self.updated_by_id = form_data.get('updated_by_id')


class FillForm(FlaskForm):
    title=StringField("Post Title:",validators=([DataRequired('Required!!'),Length(1,250,message="Title must be between 1 and 250 character")]),render_kw={"placeholder": "Post title","id":"movie-title"})
    subtitle=StringField("Subtitle:",validators=([DataRequired('Required!!')]))
    # date=StringField("Published Date:",validators=([DataRequired('Required!!')]))
    body=CKEditorField("Description:", validators=([DataRequired('Required!!')]))
    author = StringField("Author:", validators=[Optional()],render_kw={"placeholder": "Leave blank to use your own  name"})
    img_url=StringField("Image Link:", validators=([DataRequired('Required!!')]))
    submit = SubmitField('Submit',render_kw={"class":"btn btn-success"})
