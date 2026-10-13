from flask import Blueprint

bp = Blueprint(
    "Configuration",
    __name__,
    url_prefix="/a",
    template_folder="templates"
)

RegisteredPermissions = [
    ("manage_users", "Manage the permissions of other users.")
    
]

from core.Configuration import routes