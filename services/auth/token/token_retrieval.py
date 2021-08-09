from flask import request
from .token_messaging import decode_auth_token




def get_token_from_header():
    headers = request.headers
    token = headers.get('Authorization').split(" ")[1]
    return token


def get_userid_from_token(token=None) -> str:
    if token is None:
        token = get_token_from_header()
    decoded = decode_auth_token(token)
    return decoded['sub']