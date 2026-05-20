import os
from dotenv import load_dotenv
from flask import Flask, g
from flask_bootstrap import Bootstrap5
from sqlalchemy import event

from models.Base import db
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect

from controllers.UserController import UserController
from models.User import User
from controllers.PostController import PostController
from models.Comment import Comment
from controllers.CommentController import CommentController

from flask_toastr import Toastr



load_dotenv()
migrate=Migrate()
app = Flask(__name__)
app.config['SECRET_KEY'] =os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)
Bootstrap5(app)
ckeditor=CKEditor(app)
toastr=Toastr(app)



# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv('DATABASE_URI')
db.init_app(app)  #connection of database to flask application
migrate.init_app(app,db)

@app.before_request
def enable_foreign_keys():
    if not getattr(g, 'fk_enabled', False):
        db.session.execute(db.text("PRAGMA foreign_keys=ON"))
        g.fk_enabled = True
#login manager
login_manager=LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



app.add_url_rule('/','home',PostController.home)
app.add_url_rule('/post/<int:post_id>','show_post',PostController.show_post)
app.add_url_rule('/add-post','add_post',PostController.add_post,methods=['GET','POST'])
app.add_url_rule('/edit-post/<int:post_id>', 'edit_post',PostController.edit_post, methods=['GET', 'POST'])
app.add_url_rule('/delete-post/<int:post_id>','delete_post',PostController.delete_post)
app.add_url_rule('/about','about',PostController.about)
app.add_url_rule('/contact','contact',PostController.contact)
app.add_url_rule('/error','error',PostController.error)




#**************************************USERS*************************************
app.add_url_rule('/register','register',UserController.register,methods=['GET','POST'])
app.add_url_rule('/login','login',UserController.login,methods=['GET','POST'])
app.add_url_rule('/logout','logout',UserController.logout)

#************************************Comments*********************************************
app.add_url_rule('/post/<int:post_id>/comment/','add_comment',CommentController.add_comment,methods=['GET','POST'])



if __name__ == "__main__":
    app.run(debug=True, port=5003)
