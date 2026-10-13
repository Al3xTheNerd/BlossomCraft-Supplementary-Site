from flask import Blueprint

bp = Blueprint(
    "_Shared",
    __name__,
    url_prefix="/",
    template_folder="templates"
)
from core._Shared.routes import *