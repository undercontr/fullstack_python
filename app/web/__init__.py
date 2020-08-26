""" web blueprint """
from flask import Blueprint

bp = Blueprint('web', __name__, template_folder="templates", url_prefix="/<lang_code>")

from app.web import routes