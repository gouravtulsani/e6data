from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from e6blogs.utils import generate_token
from e6blogs.auth import login_required
from e6blogs.validators import (
    RegisterUserSchema, LoginSchema
)
from e6blogs.models import User


user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route("/all", methods=["GET"])
@login_required
def list_users():
    """
    Users Listing API.
    ---
    tags:
      - Users
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - APIKeyHeader: ['Authorization']

    responses:
      200:
        description: Successful operation
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
    """
    users = User().query_all({})
    for u in users:
        u.pop('password')
        u.pop('auth_token')

    return jsonify({"status": "success", "details": users})


@user_bp.route("/register", methods=["POST"])
def add_user():
    """
    User Registration API.
    ---
    tags:
      - Users
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - APIKeyHeader: ['Authorization']
    parameters:
      - in: body
        name: body
        schema:
          properties:
            first_name:
              example: abcd
            last_name:
              example: wxyz
            email:
              example: abcd@xyz.com
            password:
              example: abcdef

    responses:
      200:
        description: Successful operation
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
    """
    try:
        data = RegisterUserSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User().query(email=data['email'])
    if user.found:
        return jsonify({"status": "fail", "msg": "email already exists!"}), 400

    data['password'] = generate_password_hash(data.get('password'))

    new_user = User().add(data)
    new_user.meta.pop('password')

    return jsonify({"status": "success", "details": new_user.meta})


@user_bp.route("/login", methods=["POST"])
def login():
    """
    User login API.
    ---
    tags:
      - Users
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - APIKeyHeader: ['Authorization']
    parameters:
      - in: body
        name: body
        schema:
          properties:
            email:
              example: abcd@xyz.com
            password:
              example: abcdef

    responses:
      200:
        description: Successful operation
      400:
        description: Bad Request
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
    """
    try:
        data = LoginSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User().query(email=data['email'])
    if not user.found:
        return jsonify({'status': 'fail', 'msg': 'user not found!'}), 400

    if not check_password_hash(user.meta.get('password'), data.get('password')):
        return jsonify({'status': 'fail', 'msg': 'Invalid email or password'}), 400

    new_token = generate_token(user.meta)
    user.login(auth_token=new_token)
    user.meta.pop('password')

    return jsonify({"status": "success", "details": user.meta})


@user_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    User logout API.
    ---
    tags:
      - Users
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - APIKeyHeader: ['Authorization']

    responses:
      200:
        description: Successful operation
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
    """
    curr_user = request.current_user
    curr_user.logout()
    return jsonify({"status": "success"})
