import jwt as jwt
from os import environ
from flask import jsonify
from time import time as time
from constants.error_messages import TOKEN_BLACKLISTED, TOKEN_INVALID, TOKEN_EXPIRED


def json_token_response(token):
    return jsonify({'token': token})


def decode_auth_token(token):

    try:
        payload = jwt.decode(token, environ.get(
            'JWT_SECRET'), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return TOKEN_INVALID


def get_bad_token_reason(token: str):
    from .token_checking import token_is_blacklisted
    if token_is_blacklisted(token) is True:
        return TOKEN_BLACKLISTED
    try:
        jwt.decode(token, environ.get(
            'JWT_SECRET'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return TOKEN_INVALID
