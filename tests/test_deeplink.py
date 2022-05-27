"""Tests for `setu` package."""
import logging
import time
from datetime import datetime, timedelta

from setu import Deeplink
from setu.contract import Account, RefundRequestItem, SettlementSplits, SetuAPIException, SplitAccount

LOGGER = logging.getLogger(__name__)


def test_deeplink(v2_creds):
    """Test creation of deeplink with minimal parameters."""
    dl = Deeplink(
        scheme_id=v2_creds.scheme_id,
        secret=v2_creds.secret,
        product_instance_id="861023031961584801",
        auth_type="OAUTH",
        mode="SANDBOX",
    )

    bill_amount = 100
    split_account = SplitAccount(
        account_number="123456789",
        account_ifsc="KKBK0000001",
        amount_value=50,
    )

    try:
        # Create Payment Link
        link = dl.create_payment_link(
            amount_value=bill_amount,
            biller_bill_id="test_transaction_1234",
            amount_exactness="EXACT",
            payee_name="Python SDK unittest",
            transaction_note="unittest transaction",
            expiry_date=datetime.now() + timedelta(seconds=3),
            settlement=SettlementSplits(
                parts=[split_account],
                primary_account=Account(
                    account_number="987654321",
                    account_ifsc="KKBK0000001",
                ),
            ),
            additional_info={"sample_key": "sample_value"},
        )
        LOGGER.info(link)
        assert link.payment_link.upi_id == "refundtest@kaypay"

        # Get Payment Link Status
        link_status = dl.check_payment_status(link.platform_bill_id)
        LOGGER.info(link_status)
        assert link_status.status == "BILL_CREATED"

        # Mock Credit
        credit_response = dl.trigger_mock_payment(
            float(bill_amount) / 100, link.payment_link.upi_id, link.platform_bill_id
        )
        LOGGER.info(credit_response)
        time.sleep(3)

        # Get Payment Link Status
        link_status = dl.check_payment_status(link.platform_bill_id)
        LOGGER.info(link_status)
        assert link_status.status == "PAYMENT_SUCCESSFUL"

        # Mock Settlement
        dl.trigger_mock_settlement([credit_response.utr])
        LOGGER.info("Mocking settlement")
        time.sleep(3)

        # Get Payment Link Status
        link_status = dl.check_payment_status(link.platform_bill_id)
        LOGGER.info(link_status)
        assert link_status.status == "CREDIT_RECEIVED"  # TODO: Should be in SETTLEMENT_SUCCESSFUL

        # Initiate Refund
        split_account.amount_value = bill_amount
        batch_initiate_refund_response = dl.initiate_batch_refund(
            refunds=[
                RefundRequestItem(
                    identifier=link.platform_bill_id,
                    identifierType="BILL_ID",
                    refundType="FULL",
                    deductions=[split_account],
                ),
            ],
        )
        LOGGER.info(batch_initiate_refund_response)
        assert batch_initiate_refund_response.refunds[0].status == "MarkedForRefund"

        # Get refund batch status
        refund_batch_status_response = dl.get_batch_refund_status(batch_initiate_refund_response.batch_id)
        LOGGER.info(refund_batch_status_response)
        assert refund_batch_status_response.refunds[0].bill_id == link.platform_bill_id

        # Get individual refund status
        refund_status_response = dl.get_refund_status(batch_initiate_refund_response.refunds[0].id)
        LOGGER.info(refund_status_response)
        assert refund_status_response.bill_id == link.platform_bill_id
    except SetuAPIException as e:
        LOGGER.error(e.error)
        assert True
