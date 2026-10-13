from flask import Flask, request, jsonify, redirect, url_for, flash
import os
import core
from core.config import server_name, server_item_name, server_tracker_script
from core.utils import register_modules
from core import config as c
from core.extensions import db, login_manager
from werkzeug.exceptions import HTTPException

# /atn.py
# secret_key = ""
from atn import secret_key


app = Flask(
    __name__, 
    instance_path = os.path.abspath(__file__),
    static_folder="_Shared/static",
    static_url_path="/static")

app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.secret_key = secret_key

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "/login" # type: ignore

@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    if request.path.startswith('/static'):
        return e.get_response()
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({"error": e.description}), e.code or 500
    if request.endpoint == "_Shared.Index":
        return e.get_response()
    flash(f"Error code: {e.code}")
    return redirect(url_for("_Shared.Index"))

@login_manager.unauthorized_handler
def unauthorized():
    flash("Error, you are not authorized to be there, you dirt dog!")
    return redirect(url_for("_Shared.Index"))

register_modules(app, core)


with app.app_context():
    db.create_all()

@app.context_processor
def navbarItems():
    config = {
        'ServerName' : server_name, # 100% keep
        'ServerItemName' : server_item_name, # 100% keep
        'ServerTrackerScript' : server_tracker_script # 100% keep
    }
    return config
