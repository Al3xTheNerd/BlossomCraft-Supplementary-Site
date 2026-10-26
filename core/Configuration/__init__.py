from flask import Blueprint

bp = Blueprint(
    "Configuration",
    __name__,
    url_prefix="/a",
    template_folder="templates"
)

RegisteredPermissions = [
    ("view_queue", "View the queue of items from Fabric Mod Uploads")
]

from core.Configuration import routes