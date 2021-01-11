import jwt
import datetime
import uuid


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


def generate_setu_headers(schemeId, secret, setuProductInstanceID):
    return {
        "Authorization": generate_bearer_JWT(schemeId, secret),
        "X-Setu-Product-Instance-ID": setuProductInstanceID
    }
