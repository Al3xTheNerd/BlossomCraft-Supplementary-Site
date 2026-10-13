from flask import Blueprint

bp = Blueprint(
    "SinglePageTools",
    __name__,
    url_prefix="/tools",
    template_folder="templates"
)

from core.SinglePageTools import routes