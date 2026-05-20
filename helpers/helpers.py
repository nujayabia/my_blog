from functools import wraps


from flask import redirect, url_for, abort, flash
from flask_login import current_user
#****************************************exception handling*********************************************
def handle_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            flash(f"Error:{e}","error")
            return redirect(url_for('error'))
    return decorated

def admin_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == "admin":
            return func(*args, **kwargs)
        else:
            flash('Unauthorized Access','error')
            abort(403)

    return decorated_view

def authors_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_author == "yes":
            return func(*args, **kwargs)
        else:
            flash('Unauthorized Access','error')
            abort(403)

    return decorated_view