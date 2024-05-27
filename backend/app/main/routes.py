import os
import uuid
from datetime import datetime
from pathlib import Path

from flask import (
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import email
from app.main import bp
from app.main.forms import ContactForm
from app.models import User


@bp.route("/")
@bp.route("/index")
def index():
    return "Hello from Flask"


@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, "staticfiles"),
        "favicon.ico",
        mimetype="images/favicon.ico",
    )
