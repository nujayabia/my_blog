import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from models.Comment import Comment
from app_class.comment_class import CommentForm,CommentData
from helpers.helpers import handle_errors,admin_only,authors_only



class CommentController:
    @staticmethod
    @handle_errors
    def show_comment():
        form = CommentForm()
        return form


    @staticmethod
    @handle_errors
    @login_required
    def add_comment(post_id):
        form = CommentForm()
        if form.validate_on_submit():
            now = datetime.datetime.now()
            year = now.year
            month = now.strftime("%B")
            day = now.day
            date = f"{day} {month},{year}"
            form_data = {
                'text': form.text.data,
                'user_id': int(current_user.id),
                'post_id':int(post_id)
            }
            form_obj = CommentData(form_data)
            print(form_data)
            Comment.addComment(form_obj)
            flash('Comment added successfully!!', 'success')
            return redirect(url_for('show_post', post_id=post_id))
        return redirect(url_for('show_post', post_id=post_id))


    @staticmethod
    @handle_errors
    def get_comments(post_id):
        comments=Comment.getAllComment(post_id)
        return comments