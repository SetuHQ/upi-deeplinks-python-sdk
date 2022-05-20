"""Endpoint module."""
from setu_python_sdk.contract import API, AUTH_TYPE_OAUTH, MODE_PRODUCTION, AuthType, Mode

SANDBOX_BASE = "https://uat.setu.co/api"
PRODUCTION_BASE = "https://prod.setu.co/api"


def get_url_path(
    endpoint: API,
    auth_type: AuthType = "JWT",
    mode: Mode = "SANDBOX",
) -> str:
    """Get URL for API.

    Args:
        endpoint (API): _description_
        auth_type (AuthType, optional): _description_. Defaults to "JWT".
        mode (Mode, optional): _description_. Defaults to "SANDBOX".

    Returns:
        str: _description_
    """
    return "{base_url}{api_version}{path}".format(
        base_url=PRODUCTION_BASE if mode == MODE_PRODUCTION else SANDBOX_BASE,
        api_version="/v2" if auth_type == AUTH_TYPE_OAUTH else "",
        path=endpoint.value,
    )
