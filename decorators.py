from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if not current_user.is_admin:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_func


def email_confirmed(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if not current_user.is_confirm:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_func