"""Tests for Endpoints module."""
from setu.contract import API
from setu.endpoint import get_url_path


def test_get_uat_v1_payment_link_path():
    """Test URL for payment links with V1 auth."""
    url = get_url_path(API.PAYMENT_LINK_BASE, "JWT", "SANDBOX")
    assert url == "https://uat.setu.co/api/payment-links"


def test_get_prod_v2_mock_payment_path():
    """Test URL for mock payment with V2 auth."""
    url = get_url_path(API.TRIGGER_MOCK_PAYMENT, "OAUTH", "PRODUCTION")
    assert url == "https://prod.setu.co/api/v2/triggers/funds/addCredit"
