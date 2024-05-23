import re
from functools import wraps
from flask import request, jsonify
from e6blogs.models import User


TOKEN_RE = re.compile("([0-9a-zA-Z]{3,})")


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_token = request.headers.get('Authorization')
        if not user_token:
            return jsonify({"msg": "Unauthorized"}), 401

        token = user_token.split()[-1]  # Split (Bearer <token>)
        if not token or not TOKEN_RE.fullmatch(token):
            return jsonify({"msg": "Unauthorized, InValid Token"}), 401

        user = User().query(auth_token=token)
        if not user.found:
            return jsonify({"msg": "Invalid auth token"}), 401

        request.current_user = user
        return func(*args, **kwargs)

    return wrapper

