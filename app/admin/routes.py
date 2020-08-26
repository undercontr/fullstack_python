from flask import render_template

from app import create_app, db
from app.admin import bp


# admin yazılacak bu site yayınlandıktan sonra yapılacak


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("admin/index.jinja2")
