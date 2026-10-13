from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from flask_login import current_user
from json import loads, dumps
from typing import Dict

from core.Configuration.models import User, Logs
from core.extensions import db
from core.Configuration.decorators import permission_level_required
from core.Configuration.models import uploadLog
from core.utils import randomCode
from core.permissions import RegisteredPermissions
from core.Configuration import bp

@bp.route('/admin/resetpass/<userID>', methods=["GET"])
@permission_level_required(90)
def ForceResetPass(userID):
    user: User | None = User.query.filter(User.id == userID).first()
    if not user:
        flash("User does not exist, try again when you're not incompetent.")
        return redirect(url_for('Configuration.ManageUsers'))
    
    if current_user.permissions > user.permissions:
        randomPass = randomCode(30)
        
        user.password = generate_password_hash(randomPass, method='pbkdf2:sha256') # type: ignore
        db.session.commit()
        uploadLog(current_user, "User", "Forced a password reset.", user.id)
        flash(f"{user.username}'s password was force reset. New Password: <code>{randomPass}</code>", "info")
        return redirect(url_for('Configuration.ManageUsers'))
    else:
        flash("You can only force a password reset on people with permissions lower than your own.")
        return redirect(url_for('Configuration.ManageUsers'))

@bp.route('/admin/manageusers')
@permission_level_required(90)
def ManageUsers():
    users = User.query.order_by(User.id).all()
    
    return render_template('Configuration/admin/manageusers.html', users=users)

@bp.route('/admin/manageuser/<userID>', methods=["GET"])
@permission_level_required(90)
def ManageUser(userID: int):
    
    user: User | None = User.query.filter(User.id == userID).first()
    if not user:
        flash("User does not exist, try again when you're not incompetent.")
        return redirect(url_for('Configuration.ManageUsers'))
    
    if current_user.permissions < user.permissions:
        flash("You can only modify permissions of those with the same level, or less than yourself.")
        return redirect(url_for('Configuration.ManageUsers'))
    user.set_image_link()
    return render_template('Configuration/admin/manageuser.html', user=user, registeredPerms = RegisteredPermissions, currentNodes = user.get_permissions())

@bp.route('/admin/manageuser/<userID>', methods=["POST"])
@permission_level_required(90)
def ManageUser_POST(userID: int):
    user: User | None = User.query.filter(User.id == userID).first()
    
    if not isinstance(user, User):
        flash("User does not exist, try again when you're not incompetent.")
        return redirect(url_for('Configuration.ManageUsers'))
    
    if current_user.permissions < user.permissions:
        flash("You may only modify permissions for those with a lower access level than yourself.")
        return redirect(url_for('Configuration.ManageUsers'))
    
    niceRequest = request.form.to_dict()
    
    match niceRequest["WhichAction"]:
        case "GeneralInfo":
            if user.username != niceRequest["Username"]:
                requestedUsername = User.query.filter(User.username == niceRequest["Username"]).all()
                if len(requestedUsername) > 0:
                    flash("Cannot have the same username as another user.")
                else:
                    user.username = niceRequest["Username"]
            user.staffRole = niceRequest["StaffRole"]
            user.maintainerStatus = niceRequest["MaintainerRole"]
            if current_user.username != user.username:
                user.permissions = int(niceRequest["GeneralPermLevel"])
            user.bio = niceRequest["Bio"]
        case "Permissions":
            currentPermissionNodes: Dict[str, bool] = user.get_permissions()
            for key in currentPermissionNodes:
                if key in niceRequest:
                    currentPermissionNodes[key] = True
                else:
                    currentPermissionNodes[key] = False
            user.permissionNodes = dumps(currentPermissionNodes)
        case "RevokePicture":
            user.hasProfileImage = "https://vzge.me/head/256/X-Steve"
        case "AllowPicture":
            user.set_image_link(True)
        case _:
            flash("Form not dectected.")
    db.session.commit()
    
    return redirect(url_for("Configuration.ManageUser", userID = user.id))

@bp.route('/admin/logs/<logType>')
@permission_level_required(90)
def viewLogs(logType):
    validTypes = ["All", "Item", "Crate", "Set", "User", "Group", "Misc Item"]
    if logType in validTypes:
        if logType == "All":
            logs = Logs.query.order_by(Logs.id.desc()).all()
        else:
            logs = Logs.query.filter(Logs.Type == logType).order_by(Logs.id.desc()).all()
        return render_template("Configuration/admin/viewLogs.html", logList = logs, logType = logType)
    
    else:
        flash("Please select a valid log type.")
        return redirect(url_for("_Shared.Index"))