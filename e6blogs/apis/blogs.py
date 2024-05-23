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
    try:
        data = ListBlogSchema().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400

    blogs = Blog().query_all(data)

    return jsonify({'status': 'success', 'details': blogs})


@blog_bp.route("/<int:blog_id>/details", methods=["GET"])
@login_required
def blog_details(blog_id):
    blog = Blog().query(blog_id=blog_id)
    if not blog.found:
        return jsonify({'status': 'fail', 'msg': 'blog not found'}), 400

    return jsonify({'status': 'success', 'details': blog.meta})


@blog_bp.route("/add", methods=["POST"])
@login_required
def create():
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
    curr_user = request.current_user
    blog = Blog().query(blog_id=blog_id, author=curr_user.meta['id'])
    if not blog.found:
        return jsonify({'status': 'fail', 'msg': 'blog not found'}), 400

    blog.delete()

    return jsonify({'status': 'success'})
