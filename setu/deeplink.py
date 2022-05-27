"""Main module."""
import logging
from datetime import datetime
from typing import Any, Callable, Dict, List

import requests
from requests import Response

from setu.auth import generate_jwt_token, generate_oauth_token
from setu.body import (
    get_batch_refund_body,
    get_create_payment_link_body,
    get_mock_credit_body,
    get_mock_settlement_body,
)
from setu.contract import (
    API,
    AUTH_TYPE_JWT,
    MODE_PRODUCTION,
    AuthType,
    BatchRefundStatusResponse,
    CreatePaymentLinkResponseData,
    InitiateBatchRefundResponse,
    MockCreditResponseData,
    Mode,
    PaymentLinkStatusResponseData,
    RefundRequestItem,
    RefundResponseItem,
    SettlementSplits,
    SetuAPIException,
    ValidationRules,
)
from setu.endpoint import get_url_path
from setu.serial import (
    BatchRefundStatusResponseSchema,
    CreatePaymentLinkResponseDataSchema,
    InitiateBatchRefundResponseDataSchema,
    MockCreditResponseDataSchema,
    PaymentLinkStatusResponseDataSchema,
    RefundResponseItemSchema,
    SetuErrorResponseSchema,
)

LOGGER = logging.getLogger(__name__)


class Deeplink:
    """The Deeplink class."""

    def __init__(
        self,
        scheme_id: str,
        secret: str,
        product_instance_id: str,
        auth_type: AuthType = "JWT",
        mode: Mode = "SANDBOX",
    ):
        """Constructor for the Deeplink class.

        Args:
            scheme_id (str): _description_
            secret (str): _description_
            product_instance_id (str): _description_
            auth_type (Literal["JWT", "OAUTH"], optional): _description_. Defaults to "JWT".
            mode (Literal["SANDBOX", "PRODUCTION"], optional): _description_. Defaults to "SANDBOX".
        """
        self.scheme_id = scheme_id
        self.secret = secret
        self.mode = mode
        self.auth_type = auth_type

        self.headers = {
            "X-Setu-Product-Instance-ID": product_instance_id,
            "Content-Type": "application/json",
        }

        self.session = requests.Session()
        self.session.hooks = {"response": lambda r, *args, **kwargs: self.exception_handler(r)}

    def regenerate_token(self):
        """Re-generate token."""
        if self.auth_type == AUTH_TYPE_JWT:
            authorization = generate_jwt_token(self.scheme_id, self.secret)
        else:
            authorization = generate_oauth_token(self.scheme_id, self.secret, self.mode)
        self.headers["Authorization"] = authorization

    @staticmethod
    def exception_handler(r: Response):
        """Exception handler."""
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError) and r.reason == "Forbidden":
                raise e
            else:
                error_response_schema = SetuErrorResponseSchema()
                raise SetuAPIException(error_response_schema.load(r.json()))

    class Decorators:
        """Decorators."""

        @staticmethod
        def auth_handler(decorated: Callable):
            """Refresh token."""

            def wrapper(deeplink, *args, **kwargs):
                try:
                    if deeplink.auth_type == AUTH_TYPE_JWT:
                        deeplink.regenerate_token()
                    return decorated(deeplink, *args, **kwargs)
                except requests.exceptions.HTTPError:
                    deeplink.regenerate_token()
                    return decorated(deeplink, *args, **kwargs)

            return wrapper

    @Decorators.auth_handler
    def create_payment_link(
        self,
        amount_value: int,
        biller_bill_id: str,
        amount_exactness: str,
        payee_name: str = None,
        transaction_note: str = None,
        expiry_date: datetime = None,
        settlement: SettlementSplits = None,
        validation_rules: ValidationRules = None,
        campaign_id: str = None,
        additional_info: Dict[str, str] = None,
    ) -> CreatePaymentLinkResponseData:
        """Generate UPI payment link."""
        payload: Dict[str, Any] = get_create_payment_link_body(
            amount_value=amount_value,
            biller_bill_id=biller_bill_id,
            amount_exactness=amount_exactness,
            payee_name=payee_name,
            transaction_note=transaction_note,
            expiry_date=expiry_date,
            settlement=settlement,
            validation_rules=validation_rules,
            campaign_id=campaign_id,
            additional_info=additional_info,
        )

        api_response = self.session.post(
            get_url_path(API.PAYMENT_LINK_BASE, self.auth_type, self.mode),
            json=payload,
            headers=self.headers,
        )
        create_payment_link_response_data_schema = CreatePaymentLinkResponseDataSchema()
        return create_payment_link_response_data_schema.load(api_response.json()['data'])

    @Decorators.auth_handler
    def check_payment_status(self, platform_bill_id: str) -> PaymentLinkStatusResponseData:
        """Check status of UPI payment link."""
        api_response = self.session.get(
            "{}/{}".format(
                get_url_path(API.PAYMENT_LINK_BASE, self.auth_type, self.mode),
                platform_bill_id,
            ),
            headers=self.headers,
        )
        payment_link_status_response_data_schema = PaymentLinkStatusResponseDataSchema()
        return payment_link_status_response_data_schema.load(api_response.json()['data'])

    @Decorators.auth_handler
    def trigger_mock_payment(self, amount_value: float, upi_id: str, platform_bill_id: str) -> MockCreditResponseData:
        """Trigger mock payment for UPI payment link.

        This API is available only on SANDBOX mode.
        """
        if self.mode == MODE_PRODUCTION:
            raise Exception("trigger_mock_payment METHOD IS IS NOT AVAILABLE IN PRODUCTION")

        payload: Dict[str, Any] = get_mock_credit_body(
            amount_value=amount_value, upi_id=upi_id, platform_bill_id=platform_bill_id
        )

        api_response = self.session.post(
            get_url_path(API.TRIGGER_MOCK_PAYMENT, self.auth_type, self.mode),
            json=payload,
            headers=self.headers,
        )
        mock_credit_response_data_schema = MockCreditResponseDataSchema()
        return mock_credit_response_data_schema.load(api_response.json()['data'])

    @Decorators.auth_handler
    def trigger_mock_settlement(self, utrs: List[str]):
        """Trigger mock settlement."""
        payload: Dict[str, Any] = get_mock_settlement_body(utrs=utrs)

        self.session.post(
            get_url_path(API.TRIGGER_MOCK_SETTLEMENT, self.auth_type, self.mode),
            json=payload,
            headers=self.headers,
        )
        return

    @Decorators.auth_handler
    def initiate_batch_refund(
        self,
        refunds: List[RefundRequestItem],
    ) -> InitiateBatchRefundResponse:
        """Initiate batch refund."""
        payload: Dict[str, Any] = get_batch_refund_body(refunds=refunds)

        api_response = self.session.post(
            "{}/batch".format(get_url_path(API.REFUNDS_BASE, self.auth_type, self.mode)),
            json=payload,
            headers=self.headers,
        )
        initiate_batch_refund_response_data_schema = InitiateBatchRefundResponseDataSchema()
        return initiate_batch_refund_response_data_schema.load(api_response.json()['data'])

    @Decorators.auth_handler
    def get_batch_refund_status(self, batch_refund_id: str) -> BatchRefundStatusResponse:
        """Get batch refund status."""
        api_response = self.session.get(
            "{}/batch/{}".format(get_url_path(API.REFUNDS_BASE, self.auth_type, self.mode), batch_refund_id),
            headers=self.headers,
        )
        batch_refund_status_response_schema = BatchRefundStatusResponseSchema()
        return batch_refund_status_response_schema.load(api_response.json()['data'])

    @Decorators.auth_handler
    def get_refund_status(self, refund_id: str) -> RefundResponseItem:
        """Get individual refund status."""
        api_response = self.session.get(
            "{}/{}".format(get_url_path(API.REFUNDS_BASE, self.auth_type, self.mode), refund_id),
            headers=self.headers,
        )
        refund_response_item_schema = RefundResponseItemSchema()
        return refund_response_item_schema.load(api_response.json()['data'])
