import jwt
import datetime
import uuid
import requests

AUTHTYPEJWT = "JWT"
AUTHTYPEOAUTH = "OAUTH"


def generate_JWT(schemeId, secret):
    payload = {
        "aud": schemeId,
        "iat": datetime.datetime.utcnow(),
        "jti": str(uuid.uuid1()),
    }

    return jwt.encode(payload, secret, algorithm="HS256")


def generate_bearer_JWT(schemeId, secret):
    return "Bearer {}".format(generate_JWT(schemeId, secret))


def verify_JWT(token, schemeId, secret):
    try:
        jwt.decode(token, secret, audience=schemeId)
    except jwt.PyJWTError:
        raise


def generate_oAuth_token(clientId, secret, url):
    url = url + "/v2/auth/token"
    payload = {
        "clientID": clientId,
        "secret": secret,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return "Bearer {}".format(data["data"]["token"])
    raise


def generate_setu_headers(
    schemeId, secret, setuProductInstanceID, url, authType=AUTHTYPEJWT
):
    headers = {
        "X-Setu-Product-Instance-ID": setuProductInstanceID,
        "Content-Type": "application/json",
    }

    if authType == AUTHTYPEJWT:
        auth = generate_bearer_JWT(schemeId, secret)
    elif authType == AUTHTYPEOAUTH:
        auth = generate_oAuth_token(schemeId, secret, url)
    else:
        raise Exception("Invalid authType")

    headers["Authorization"] = auth

    return headers
