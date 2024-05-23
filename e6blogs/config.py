import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_POOL_PRE_PING = True
    SECRET_KEY = b'\xdc\xde\x16\xf9\x99\x06\ry\x84U\xfd-5~n\xdf'
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = 'production'
