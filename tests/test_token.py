from constants.token import TOKEN_DEFAULT_TIME_IN_MINUTES
from constants.error_messages import TOKEN_INVALID
import pytest
from pytest import MonkeyPatch
from services.auth.token import check_auth_token, token_about_to_expire, create_user_auth_token, get_userid_from_token,decode_auth_token
try:
    from app import app

except ImportError:
    from __main__ import app

a_bad_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Mjc2MDQxOTUsImlhdCI6MTYyNzU5MzM5NSwic3ViIjoiNzA1ZmJjMzItOTBhMS00ZGI2LTllMDktOGNlNzFhZWY1YTZmIn0.AdJVrswhNvwA66WLoOciEvbCNvVDWLq5f1dACe84fW4"
a_user_id = "1234"
TEST_JWT_SECRET = "RzDGEEvvy7H5ptUJzjFapBXMGPTFPkWwJcNdt8jRQDL4VwCksU7E7U4Dky9YuHk3KKS3HMJqf64NdhJvNFKKrqdnMYbRx8K7utK2Qk2W2GA5P9atFx3GLRTaFGR3rcKJ"
mp = MonkeyPatch()
mp.setenv("JWT_SECRET", TEST_JWT_SECRET)

@pytest.fixture
def good_token():
    return create_user_auth_token(user_id=a_user_id)



@pytest.fixture
def bad_token():
    return a_bad_token

def test_valid_token(good_token):
    valid = check_auth_token(good_token, check_blacklist=False)
    assert valid is True

def test_invalid_token(bad_token):
    valid = check_auth_token(bad_token, check_blacklist=False)
    assert valid == False

def test_expired_invalid_token(bad_token):
    assert decode_auth_token(bad_token) == TOKEN_INVALID

def test_userid_from_token(good_token):
    assert get_userid_from_token(good_token) == a_user_id

def test_token_not_about_to_expire(good_token):
    assert token_about_to_expire(token=good_token) == False

def test_token_is_about_to_expire(good_token):
    assert token_about_to_expire(token=good_token, threshold=TOKEN_DEFAULT_TIME_IN_MINUTES+1) == True
    



