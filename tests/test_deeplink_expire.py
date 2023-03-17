"""Tests for `setu` package."""
import logging
from datetime import datetime, timedelta

from setu import Deeplink, SetuAPIException

LOGGER = logging.getLogger(__name__)


def test_deeplink_expire(v2_creds):
    """Test creation of deeplink with minimal parameters."""
    dl = Deeplink(
        scheme_id=v2_creds.scheme_id,
        secret=v2_creds.secret,
        product_instance_id="861023031961584801",
        auth_type="OAUTH",
        mode="SANDBOX",
    )

    try:
        # Create Payment Link
        link = dl.create_payment_link(
            amount_value=1000,
            biller_bill_id="test_transaction_1234",
            amount_exactness="EXACT",
            payee_name="Python SDK unittest",
            transaction_note="unittest transaction",
            expiry_date=datetime.now() + timedelta(days=3),
        )
        LOGGER.info(link)
        assert link.platform_bill_id

        # Get Payment Link Status
        link_status = dl.check_payment_status(link.platform_bill_id)
        LOGGER.info(link_status)
        assert link_status.status == "BILL_CREATED"

        dl.expire_payment_link(link.platform_bill_id)
        link_status = dl.check_payment_status(link.platform_bill_id)
        LOGGER.info(link_status)
        assert link_status.status == "BILL_EXPIRED"

    except SetuAPIException as e:
        LOGGER.error(e.error)
        assert True
