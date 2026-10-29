from flask import Blueprint

bp = Blueprint(
    "Votes",
    __name__,
    url_prefix="/votes",
    template_folder="templates"
)

from core.Votes import routes