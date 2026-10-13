from functools import wraps
from flask_login import login_required, current_user
from flask import flash, redirect, url_for

def permission_level_required(level: int):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.permissions < level:
                flash(f"You need <code>Level: {level}</code> permission to view that page. Current: <code>Level: {current_user.permissions}</code>.")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator