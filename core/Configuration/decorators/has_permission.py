from functools import wraps
from flask_login import login_required, current_user
from flask import flash, redirect, url_for
from core.Configuration.models import User
def has_permission(perm: str):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(perm):
                flash(f"You need <code>Permission: {perm}</code> to view that page.")
                return redirect(url_for('Configuration.Index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator