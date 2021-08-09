from models.user import User
from constants.error_messages import NOT_ALLOWED, TOKEN_DOESNT_EXIST, TOKEN_INVALID
from common.responses import json_response
from functools import wraps
from services.auth.token import check_auth_token, get_bad_token_reason, get_token_from_header, get_userid_from_token
from flask import request


def auth_required(f):
    @wraps(f)
    def _auth_required(*args, **kwargs):
        headers = request.headers

        if 'Authorization' in headers:
            try:

                # If the token is invalid, stop there
                token = get_token_from_header()
                status = check_auth_token(token)
                if status == False:
                    return json_response(get_bad_token_reason(token), 401)

                # If the user account does not exist, stop there
                user_id = get_userid_from_token(token)
                user = User.query.filter(User.id == user_id).first()

                if user is None:
                    return json_response(NOT_ALLOWED, 401)

            except:
                return json_response(TOKEN_INVALID, 401)

        else:
            return json_response(TOKEN_DOESNT_EXIST, 401)

        return f(*args, **kwargs)

    return _auth_required
