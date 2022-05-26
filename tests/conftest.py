"""Common PyTest fixtures to be consumed in tests."""
import pytest

from setu_python_sdk.contract import APICredentials


@pytest.fixture
def v1_creds() -> APICredentials:
    """Fixture to get V1 creds."""
    return APICredentials(
        scheme_id="5bf4376b-6008-43c8-8ce0-a5ea196e3091",
        secret="9975fd99-d5ed-416a-9963-5d113dc80582",
    )


@pytest.fixture
def v2_creds() -> APICredentials:
    """Fixture to get V2 creds."""
    return APICredentials(
        scheme_id="c4f57443-dc1e-428f-8c4e-e5fd531057d2",
        secret="5b288618-473f-4193-ae1b-8c42f223798e",
    )
