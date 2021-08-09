
from common.responses import json_response
from models.blacklist import BlacklistToken
from constants.token import TOKEN_DEFAULT_TIME_IN_MINUTES
import jwt as jwt
import datetime
from os import environ

from time import time as time
from constants.error_messages import SERVER_ERROR


def create_user_auth_token(**kwargs):
    try:

        previous_token = kwargs.get('previous_token')

        if previous_token is not None:
            # add the previous token to the blacklist
            on_blacklist = BlacklistToken.check_for_blacklist(previous_token)

            if on_blacklist is False:
                bl_token = BlacklistToken(previous_token)
                blacklisted = bl_token.add_token_to_blacklist()

                if (blacklisted == False):
                    return json_response(SERVER_ERROR, 500)

        secret = environ.get('JWT_SECRET')
        user_id = kwargs.get("user_id")

        if isinstance(user_id, str) == False:
            user_id = str(user_id)

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_DEFAULT_TIME_IN_MINUTES),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(
            payload,
            secret,
            algorithm='HS256'
        )

        return token

    except Exception as e:
        return False
