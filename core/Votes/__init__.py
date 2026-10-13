from flask import Blueprint

bp = Blueprint(
    "Votes",
    __name__,
    url_prefix="/votes"
)

from core.Votes import routes