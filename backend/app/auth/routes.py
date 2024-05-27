from urllib.parse import urlparse as url_parse

import requests
from flask import (
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from password_strength import PasswordStats

from app import db, email, flash_errors
from app.auth import bp
from app.auth.manager import Manager as manager
from app.auth.password import validate_policy, validate_strength
from app.models import Role, User
