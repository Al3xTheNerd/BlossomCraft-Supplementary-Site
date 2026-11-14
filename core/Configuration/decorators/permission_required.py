from functools import wraps
from flask_login import login_required, current_user
from flask import flash, redirect, url_for, request, jsonify
from core.Configuration.models.user import User


def permission_level_required(level: int):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if (current_user.permissions or 0) < level:
                flash(f"You need <code>Level: {level}</code> permission to view that page. Current: <code>Level: {current_user.permissions}</code>.")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def api_permission_level_required(level: int):
    """Token authentication decorator for Fabric mod REST endpoints."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"success": False, "error": "Missing or invalid authorization token"}), 401

            token = auth_header.split(" ", 1)[1].strip()

            user = None
            if hasattr(User, "api_token"):
                try:
                    user = User.query.filter_by(api_token=token).first()
                except Exception:
                    User.query.session.rollback()
            if not user and hasattr(User, "token"):
                try:
                    user = User.query.filter_by(token=token).first()
                except Exception:
                    User.query.session.rollback()
            if not user and hasattr(User, "password"):
                try:
                    user = User.query.filter_by(password=token).first()
                except Exception:
                    User.query.session.rollback()

            if not user:
                return jsonify({"success": False, "error": "Invalid token"}), 401

            if (getattr(user, "permissions", 0) or 0) < level:
                return jsonify({"success": False, "error": "Insufficient permissions"}), 403

            return f(user, *args, **kwargs)
        return decorated_function
    return decorator