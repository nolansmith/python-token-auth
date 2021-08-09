from flask.testing import FlaskClient
import pytest
try:
    from app import app

except ImportError:
    from __main__ import app

from constants.error_messages import RESOURCE_NOT_FOUND


@pytest.fixture
def client():
    return app.test_client()


def test_bad_resource(client: FlaskClient):
    res = client.get('/')
    assert res.status_code == 404
    assert res.json.get('message', RESOURCE_NOT_FOUND)
