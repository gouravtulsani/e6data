from datetime import datetime
from marshmallow import Schema, fields, validate


class RegisterUserSchema(Schema):
    first_name = fields.Str(validate=validate.Length(min=3, max=20))
    last_name = fields.Str(validate=validate.Length(min=3, max=20))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    created_at = fields.Str(load_default=datetime.now().strftime('%Y%m%d'))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class AddBlogSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    content = fields.Str(required=True, validate=validate.Length(min=3))
    created_at = fields.Str(load_default=datetime.now().strftime('%Y%m%d'))


class UpdateBlogSchema(Schema):
    title = fields.Str(validate=validate.Length(min=3, max=50))
    content = fields.Str(validate=validate.Length(min=3))


class ListBlogSchema(Schema):
    author = fields.Int()
    created_at = fields.Int()
    cursor = fields.Int()
