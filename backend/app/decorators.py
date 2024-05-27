from functools import wraps

from flask import abort, request
from flask_login import current_user

import app

from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


def require_appkey(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (
            not request.args.get("key")
            and not request.args.get("key") == app.config["API_KEY"]
        ):
            abort(401)
        return f(*args, kwargs)

    return decorated_function
