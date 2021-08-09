
from models.blacklist import BlacklistToken
from constants.token import TOKEN_REFRESH_THRESHOLD_IN_MINUTES
import jwt as jwt
from os import environ
from time import time as time
from constants.error_messages import TOKEN_BLACKLISTED, TOKEN_INVALID, TOKEN_EXPIRED
from common.utils import destructure
from .token_retrieval import get_token_from_header
from .token_messaging import decode_auth_token

def check_auth_token(token, check_blacklist=True) -> bool:

    if check_blacklist is True:
        if token_is_blacklisted(token=token) is True:
            return False

    if isinstance(token, str):
        return decode_auth_token(token) not in [TOKEN_INVALID, TOKEN_EXPIRED, TOKEN_BLACKLISTED]
    return False


def token_about_to_expire(**kwargs) -> bool:
    token = kwargs.get("token")

    if token is None:
        token = get_token_from_header()

    decoded = decode_auth_token(token)
    [exp] = destructure(decoded, 'exp')
    minutes_left = (int(exp) - int(time()))/60

    threshold = kwargs.get("threshold")

    if threshold is None:
        threshold = TOKEN_REFRESH_THRESHOLD_IN_MINUTES

    if (minutes_left <= threshold):

        return True
    else:
        return False


def token_is_blacklisted(**kwargs):
    token = kwargs.get('token')
    blacklisted = BlacklistToken.check_for_blacklist(token)
    return blacklisted
