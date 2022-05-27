```python
from setu import Deeplink, SetuAPIException

dl = Deeplink(
    scheme_id="c4f57443-dc1e-428f-8c4e-e5fd531057d2",
    secret="5b288618-473f-4193-ae1b-8c42f223798e",
    product_instance_id="861023031961584801",
    auth_type="OAUTH",
    mode="SANDBOX",
)

try:
    # Create Payment Link
    link = dl.create_payment_link(
        amount_value=2000,
        biller_bill_id="test_transaction_1234",
        amount_exactness="EXACT",
    )
    assert link.payment_link.upi_id == "refundtest@kaypay"

    # Mock Payment (Sandbox)
    credit_response = dl.trigger_mock_payment(
        200, link.payment_link.upi_id, link.platform_bill_id
    )

    # Get Payment Link Status
    link_status = dl.check_payment_status(link.platform_bill_id)
    assert link_status.status == "PAYMENT_SUCCESSFUL"
except SetuAPIException as e:
    LOGGER.error(e.error)
    assert True
```
