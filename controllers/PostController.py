import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import date

from flask_login import login_required, current_user

from controllers.CommentController import CommentController
from models.Post import BlogPost
from app_class.post_class import FillForm,PostData
from helpers.helpers import handle_errors,admin_only,authors_only
from models.Comment import Comment


class PostController:

    @staticmethod
    # @handle_errors
    def home():
        page = request.args.get('page', 1, type=int)
        per_page=3
        if current_user.is_authenticated and current_user.role=='user':
            posts_paginated = BlogPost.get_query_by_user(current_user.id).paginate(page=page, per_page=per_page, error_out=False)
        else:
            posts_paginated = BlogPost.getQuery().paginate(page=page, per_page=per_page, error_out=False)
        print(posts_paginated)
        return render_template("index.html", all_posts=posts_paginated)

    @staticmethod
    @handle_errors
    @authors_only
    def add_post():
        form = FillForm()
        if form.validate_on_submit():
            now = datetime.datetime.now()
            year = now.year
            month = now.strftime("%B")
            day = now.day
            date = f"{day} {month},{year}"
            form_data = {
                'title': form.title.data,
                'subtitle': form.subtitle.data,
                'date': date,
                'body': form.body.data,
                'author': form.author.data,
                'img_url': form.img_url.data,
                'added_by_id': int(current_user.id)
            }
            form_obj = PostData(form_data)
            print(form_data)
            print(form_obj.added_by_id)
            BlogPost.addPost(form_obj)
            flash('Post added successfully!!', 'success')
            return redirect(url_for('home'))
        return render_template("make-post.html", form=form, pagename="add")

    @staticmethod
    @handle_errors
    @login_required
    @admin_only
    def edit_post(post_id):
        print("reached controller")
        post_data = BlogPost.getPost(post_id)
        form = FillForm(obj=post_data)
        if form.validate_on_submit():
            form_data = {
                'title': form.title.data,
                'subtitle': form.subtitle.data,
                'date': date,
                'body': form.body.data,
                'author': form.author.data,
                'img_url': form.img_url.data,
                'updated_by_id': current_user.id
            }
            form_obj = PostData(form_data)
            BlogPost.editPost(form_obj, post_id)
            flash('Blog edited succesfully.', 'success')
            return redirect(url_for('home'))
        return render_template('make-post.html', form=form, pagename="edit")

    @staticmethod
    @handle_errors
    @admin_only
    def delete_post(post_id):
        BlogPost.deletePost(post_id)
        flash('Post successfully deleted', 'success')
        return redirect(url_for('home'))

    @staticmethod
    @handle_errors
    def show_post(post_id):
        requested_post = BlogPost.getPost(post_id)
        form=CommentController.show_comment()
        comments=CommentController.get_comments(post_id)
        return render_template("post.html", comments=comments,form=form,post=requested_post)

    @staticmethod
    def about():
        return render_template("about.html")

    @staticmethod
    def contact():
        return render_template("contact.html")

    @staticmethod
    @handle_errors
    def error():
        return render_template("error.html")
