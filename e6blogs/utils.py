import time
import hashlib


def generate_token(user):
    key = f"{user.get('email')}-{str(time.time())}"
    hash_object = hashlib.sha256(bytes(key, 'utf-8'))
    return hash_object.hexdigest()


def jsonify(header, data, many=True):
    if many:
        if not data:
            return []
        data = [dict(zip(header, d)) for d in data]
        return data

    if not data:
        return {}
    data = dict(zip(header, data))
    return data
