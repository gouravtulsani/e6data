from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from e6blogs.auth import login_required
from e6blogs.validators import (
    AddBlogSchema, UpdateBlogSchema, ListBlogSchema
)
from e6blogs.models import Blog


blog_bp = Blueprint('blog', __name__, url_prefix='/api/blog')


@blog_bp.route("/all", methods=["GET"])
@login_required
def list_all_blogs():
    """
    Blogs Listing API.
    ---
    tags:
      - Blogs
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - APIKeyHeader: ['Authorization']
    parameters:
      - in: query
        name: author
        type: integer
        description: filter for blogs
      - in: query
        name: created_at
        type: integer
        description: filter for blogs `YYYYMMDD` format
      - in: query
        name: cursor
        type: integer
        description: for pagination (last blog id.)
        default: 0

    responses:
      200:
        description: Successful operation
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
    """
    try:
        data = ListBlogSchema().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400

    blogs = Blog().query_all(data)

    return jsonify({'status': 'success', 'details': blogs})


@blog_bp.route("/<int:blog_id>/details", methods=["GET"])
@login_required
def blog_details(blog_id):
    """
        Blogs Detail API.
        ---
        tags:
          - Blogs
        consumes:
          - application/json
        produces:
          - application/json
        security:
          - APIKeyHeader: ['Authorization']
        parameters:
          - in: path
            name: blog_id
            type: integer
            required: true

        responses:
          200:
            description: Successful operation
          401:
            description: Unauthorized Request
          500:
            description: Internal Server Error
        """
    blog = Blog().query(blog_id=blog_id)
    if not blog.found:
        return jsonify({'status': 'fail', 'msg': 'blog not found'}), 400

    return jsonify({'status': 'success', 'details': blog.meta})


@blog_bp.route("/add", methods=["POST"])
@login_required
def create():
    """
    Add Blog API.
    ---
    tags:
      - Blogs
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
            title:
              example: "Blog's title"
            content:
              example: "Blog's body content goes here"

    responses:
      200:
        description: Successful operation
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
        """
    curr_user = request.current_user
    try:
        data = AddBlogSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    data['author'] = curr_user.meta['id']

    blog = Blog().add(data)

    return jsonify({'status': 'success', 'details': blog.meta})


@blog_bp.route("/<int:blog_id>/update", methods=["POST"])
@login_required
def update(blog_id):
    """
    Blog Update API.
    ---
    tags:
      - Blogs
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - APIKeyHeader: ['Authorization']
    parameters:
      - in: path
        name: blog_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          properties:
            title:
              example: "Updated Title"
            content:
              example: "Updated Content"

    responses:
      200:
        description: Successful operation
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
    """
    curr_user = request.current_user
    try:
        data = UpdateBlogSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    blog = Blog().query(blog_id=blog_id, author=curr_user.meta['id'])
    if not blog.found:
        return jsonify({'status': 'fail', 'msg': 'blog not found'}), 400

    blog.update(data)

    return jsonify({'status': 'success', 'details': blog.meta})


@blog_bp.route("/<int:blog_id>/delete", methods=["DELETE"])
@login_required
def delete(blog_id):
    """
    Blog Delete API.
    ---
    tags:
      - Blogs
    consumes:
      - application/json
    produces:
      - application/json
    security:
      - APIKeyHeader: ['Authorization']
    parameters:
      - in: path
        name: blog_id
        type: integer

    responses:
      200:
        description: Successful operation
      401:
        description: Unauthorized Request
      500:
        description: Internal Server Error
    """
    curr_user = request.current_user
    blog = Blog().query(blog_id=blog_id, author=curr_user.meta['id'])
    if not blog.found:
        return jsonify({'status': 'fail', 'msg': 'blog not found'}), 400

    blog.delete()

    return jsonify({'status': 'success'})
