"""Marshmallow serialization classes."""
import logging

from marshmallow import EXCLUDE, Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from setu_python_sdk.contract import (
    Account,
    Amount,
    BatchRefundStatusResponse,
    CreatePaymentLinkResponseData,
    InitiateBatchRefundResponse,
    MockCreditResponseData,
    PaymentLink,
    PaymentLinkStatusResponseData,
    Receipt,
    RefundResponseItem,
    SetuErrorResponseData,
)

LOGGER = logging.getLogger(__name__)


class SetuResponseBaseSchema(Schema):
    """Setu Base Response Schema."""

    status = fields.Int()
    success = fields.Bool()


class SetuErrorResponseDataSchema(Schema):
    """Setu Error Response Data Schema."""

    code = fields.Str()
    detail = fields.Str()
    title = fields.Str()
    doc_url = fields.Str(data_key="docURL", required=False)
    errors = fields.List(fields.Str(), required=False)
    trace_id = fields.Str(data_key="traceID", required=False)

    @post_load
    def make_error_response_data(self, data, **kwargs):
        """Deserialize to SetuErrorResponseData object."""
        return SetuErrorResponseData(**data)


class SetuErrorResponseSchema(SetuResponseBaseSchema):
    """Setu Error Response Schema."""

    error_response = fields.Nested(SetuErrorResponseDataSchema(), data_key="error")

    @post_load
    def make_error_response(self, data, **kwargs):
        """Deserialize to SetuErrorResponseData object."""
        return data["error_response"]


class PaymentLinkSchema(Schema):
    """Payment Link information schema."""

    short_url = fields.Str(data_key="shortURL", required=False)
    upi_id = fields.Str(data_key="upiID")
    upi_link = fields.Str(data_key="upiLink")

    @post_load
    def make_payment_link(self, data, **kwargs):
        """Deserialize to PaymentLink object."""
        return PaymentLink(**data)


class CreatePaymentLinkResponseDataSchema(Schema):
    """Create Payment Link Response Data Schema."""

    name = fields.Str()
    payment_link = fields.Nested(PaymentLinkSchema(), data_key="paymentLink")
    platform_bill_id = fields.Str(data_key="platformBillID")
    campaign_id = fields.Str(data_key="campaignID")

    @post_load
    def make_create_payment_link_response(self, data, **kwargs):
        """Deserialize to CreatePaymentLinkResponseData object."""
        return CreatePaymentLinkResponseData(**data)


class AmountSchema(Schema):
    """Amount Schema."""

    currency_code = fields.Str(data_key="currencyCode")
    value = fields.Int()

    @post_load
    def make_amount(self, data, **kwargs):
        """Deserialize to Amount object."""
        return Amount(**data)


class ReceiptSchema(Schema):
    """Receipt Schema."""

    date = fields.DateTime()
    id = fields.Str()

    @post_load
    def make_receipt(self, data, **kwargs):
        """Deserialize to Receipt object."""
        return Receipt(**data)


class PaymentLinkStatusResponseDataSchema(Schema):
    """Payment Link Status Response Data Schema."""

    created_at = fields.DateTime(data_key="createdAt")
    expires_at = fields.DateTime(data_key="expiresAt")
    name = fields.Str()
    payment_link = fields.Nested(PaymentLinkSchema(), data_key="paymentLink")
    platform_bill_id = fields.Str(data_key="platformBillID")
    biller_bill_id = fields.Str(data_key="billerBillID")
    status = fields.Str()
    transaction_note = fields.Str(data_key="transactionNote")
    campaign_id = fields.Str(data_key="campaignID", required=False)
    payer_vpa = fields.Str(data_key="payerVpa", required=False)
    receipt = fields.Nested(ReceiptSchema(), required=False)
    amount_paid = fields.Nested(AmountSchema(), data_key="amountPaid", required=False)
    additional_info = fields.Dict(keys=fields.Str(), values=fields.Str(), data_key="additionalInfo", required=False)

    @post_load
    def make_payment_link_status_response(self, data, **kwargs):
        """Deserialize to PaymentLinkStatusResponseData."""
        return PaymentLinkStatusResponseData(**data)


class MockCreditResponseDataSchema(Schema):
    """Mock Credit Response Data Schema."""

    utr = fields.Str()

    @post_load
    def make_mock_credit_response(self, data, **kwargs):
        """Deserialize to MockCreditResponseData."""
        return MockCreditResponseData(**data)


class AccountSchema(Schema):
    """Account Schema."""

    account_number = fields.Str(data_key="id")
    account_ifsc = fields.Str(data_key="ifsc")
    name = fields.Str(required=False)

    @post_load
    def make_account(self, data, **kwargs):
        """Deserialize to Account object."""
        return Account(**data)


class SplitDetailsSchema(Schema):
    """Split Details Schema."""

    value = fields.Int()
    unit = fields.Str()


class DeductionResponseSchema(Schema):
    """Deduction Response Schema."""

    account = fields.Nested(AccountSchema())
    split = fields.Nested(SplitDetailsSchema())


class RefundResponseItemSchema(Schema):
    """Refund Response Item Schema."""

    id = fields.Str()
    bill_id = fields.Str(data_key="billID")
    transaction_ref_id = fields.Str(data_key="transactionRefID")
    amount = fields.Nested(AmountSchema())
    status = fields.Str()
    deductions = fields.List(fields.Nested(DeductionResponseSchema()), required=False)
    initiated_at = fields.DateTime(data_key="initiatedAt", required=False)

    @post_load
    def make_refund_response_item(self, data, **kwargs):
        """Deserialize to RefundResponseItem object."""
        return RefundResponseItem(**data)


class BatchRefundResponseItemSchema(OneOfSchema):
    """Batch Refund Response Data Item Schema."""

    type_field = "success"
    type_schemas = {True: RefundResponseItemSchema, False: SetuErrorResponseDataSchema}

    seq_no = fields.Int(data_key="seqNo")
    success = fields.Bool()


class InitiateBatchRefundResponseDataSchema(Schema):
    """Initiate Batch Refund Response Data Schema."""

    batch_id = fields.Str(data_key="batchID")
    refunds = fields.List(fields.Nested(BatchRefundResponseItemSchema(unknown=EXCLUDE)))

    @post_load
    def make_initiate_batch_refund_response_data(self, data, **kwargs):
        """Deserialize to InitiateBatchRefundResponse object."""
        return InitiateBatchRefundResponse(**data)


class BatchRefundStatusResponseSchema(Schema):
    """Get Batch Refund Status Response Data Schema."""

    batch_id = fields.Str(data_key="batchID")
    refunds = fields.List(fields.Nested(RefundResponseItemSchema()))

    @post_load
    def make_batch_refund_response(self, data, **kwargs):
        """Deserialize to BatchRefundStatusResponse object."""
        return BatchRefundStatusResponse(**data)
