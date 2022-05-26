"""Auth module."""
import datetime
import uuid

import jwt
import requests

from setu_python_sdk.contract import API, AUTH_TYPE_OAUTH, Mode
from setu_python_sdk.endpoint import get_url_path


def generate_jwt_token(scheme_id: str, secret: str) -> str:
    """Generate a JWT token.

    Args:
        scheme_id (str): _description_
        secret (str): _description_

    Returns:
        str: _description_
    """
    payload = {
        "aud": scheme_id,
        "iat": datetime.datetime.utcnow(),
        "jti": str(uuid.uuid1()),
    }

    return "Bearer {}".format(jwt.encode(payload, secret, algorithm="HS256"))


def generate_oauth_token(
    client_id: str,
    secret: str,
    mode: Mode = "SANDBOX",
) -> str:
    """Generate an OAuth token.

    Args:
        client_id (str): _description_
        secret (str): _description_
        mode (Mode, optional): _description_. Defaults to "SANDBOX".

    Returns:
        str: _description_
    """
    payload = {
        "clientID": client_id,
        "secret": secret,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        get_url_path(API.FETCH_TOKEN, AUTH_TYPE_OAUTH, mode),
        json=payload,
        headers=headers,
    )

    if response.status_code == 200:
        data = response.json()
        return "Bearer {}".format(data["data"]["token"])
    raise
