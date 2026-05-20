from flask import Flask, render_template, redirect, url_for,flash
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from models.Base import db
from models.User import User
from app_class.user_class import UserForm,UserData,LoginForm
from flask_login import login_required, login_user, current_user, logout_user
from helpers.helpers import handle_errors



class UserController:

    @staticmethod
    @handle_errors
    def register():
        form=UserForm()
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if form.validate_on_submit():
            if User.getByParam(email=form.email.data):
                flash("Email already has been taken", "error")
                return render_template('register.html', form=form, pagename="register")
            hash_password=generate_password_hash(form.password.data,method="pbkdf2:sha256",salt_length=8)
            user_data={
                'name':form.name.data,
                'email':form.email.data,
                'password':hash_password
            }
            user_obj=UserData(user_data)
            User.addUser(user_obj)
            flash("User has been successfully added.",'success')
            return redirect(url_for('home'))
        return render_template('register.html',form=form,pagename="register")


    @staticmethod
    @handle_errors
    def login():
        form=LoginForm()
        if form.validate_on_submit():
            query = select(User).where(User.email == form.email.data)
            user = db.session.execute(query).scalar()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Dear {current_user.name},Welcome to dashboard", "success")
                return redirect(url_for("home"))
            else:
                flash("Sorry,Wrong Credentials!!", "error")
        return render_template('login.html',loginform=form,pagename="login")



    @staticmethod
    @handle_errors
    @login_required
    def logout():
        logout_user()
        flash("Logged out Successfully!!.Please visit us again", "info")
        return redirect(url_for("home"))


