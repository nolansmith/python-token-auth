from common.responses import json_response
from services.auth.token import check_auth_token, create_user_auth_token, get_bad_token_reason, get_token_from_header, get_userid_from_token, json_token_response, token_about_to_expire
from common.decorators.auth import auth_required
from flask import Blueprint
from flask_cors import cross_origin


token_routes = Blueprint("token_routes", __name__, url_prefix='/token')


@token_routes.route('/check', methods=['POST'])
@cross_origin()
def check_token_validity():
    token = get_token_from_header()
    valid = check_auth_token(token)
    message = 'Valid token check'
    if valid is False:
        message = get_bad_token_reason(token)

    return json_response(message, 200, valid=valid)


@token_routes.route('/refresh', methods=['POST'])
@cross_origin()
# must have valid token to get a refresh
@auth_required
def refresh_auth_token():
    expiring = token_about_to_expire()

    # if the token is near expiration, create a new one
    # if it isn't, keep the current one
    # this will keep the future token blacklist length down
    if expiring is True:
        token = get_token_from_header()
        user_id = get_userid_from_token()
        new_token = create_user_auth_token(
            user_id=user_id, previous_token=token)
        return json_token_response(new_token)
    else:
        token = get_token_from_header()
        return json_token_response(token)
