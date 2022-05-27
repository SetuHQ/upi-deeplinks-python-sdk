"""Tests for Auth module."""
import jwt

from setu.auth import generate_jwt_token, generate_oauth_token


def test_generate_jwt_token(v1_creds):
    """Test generation of JWT token."""
    bearer_token = generate_jwt_token(v1_creds.scheme_id, v1_creds.secret)
    jwt_token = bearer_token[bearer_token.startswith("Bearer ") and len("Bearer ") :]

    payload = jwt.decode(jwt_token, options={"verify_signature": False})
    assert payload["aud"] == v1_creds.scheme_id


def test_generate_oauth_token(v2_creds):
    """Test generation of OAuth token."""
    bearer_token = generate_oauth_token(v2_creds.scheme_id, v2_creds.secret, "SANDBOX")
    jwt_token = bearer_token[bearer_token.startswith("Bearer ") and len("Bearer ") :]

    payload = jwt.decode(jwt_token, options={"verify_signature": False})
    assert payload["clientId"] == v2_creds.scheme_id
