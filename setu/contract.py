"""Contract module."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Union

# Auth types
AuthType = str  # TODO: Figure out a way to use Literal["JWT", "OAUTH"] across Python versions
AUTH_TYPE_JWT: AuthType = "JWT"
AUTH_TYPE_OAUTH: AuthType = "OAUTH"

# Modes
Mode = str  # TODO: Figure out a way to use Literal["SANDBOX", "PRODUCTION"] across Python versions
MODE_SANDBOX: Mode = "SANDBOX"
MODE_PRODUCTION: Mode = "PRODUCTION"


# Paths
class API(Enum):
    """Enum containing all the API paths supported by SDK."""

    FETCH_TOKEN = "/auth/token"
    PAYMENT_LINK_BASE = "/payment-links"
    TRIGGER_MOCK_PAYMENT = "/triggers/funds/addCredit"
    TRIGGER_MOCK_SETTLEMENT = "/triggers/funds/mockSettlement"
    EXPIRE_BILL = "/utilities/bills/{}/expire"
    REPORTS_BASE = "/reports"
    REFUNDS_BASE = "/refund"


class APICredentials(NamedTuple):
    """API Credential information."""

    scheme_id: str
    secret: str


@dataclass
class SetuResponseBase:
    """Setu base response."""

    success: bool
    status: int


@dataclass
class SetuErrorResponseData:
    """Setu error response data."""

    code: str
    detail: str
    title: str
    doc_url: Optional[str] = None
    errors: Optional[List[Any]] = None
    trace_id: Optional[str] = None


@dataclass
class SetuAPIException(Exception):
    """Setu exception class."""

    error: SetuErrorResponseData


@dataclass
class PaymentLink:
    """Payment Link information."""

    upi_id: str
    upi_link: str
    short_url: Optional[str] = None


@dataclass
class CreatePaymentLinkResponseData:
    """Response from Create Payment Link API."""

    name: str
    payment_link: PaymentLink
    platform_bill_id: str
    campaign_id: Optional[str] = None


@dataclass
class Amount:
    """Amount information."""

    currency_code: str
    value: int


@dataclass
class Receipt:
    """Payment receipt information."""

    date: datetime
    id: str


@dataclass
class PaymentLinkStatusResponseData:
    """Response from Payment Link Status API."""

    created_at: datetime
    expires_at: datetime
    name: str
    payment_link: PaymentLink
    platform_bill_id: str
    biller_bill_id: str
    status: str
    transaction_note: str
    campaign_id: Optional[str] = None
    payer_vpa: Optional[str] = None
    receipt: Optional[Receipt] = None
    amount_paid: Optional[int] = None
    additional_info: Optional[Dict[str, str]] = None


@dataclass
class Account:
    """Bank account information."""

    account_number: str
    account_ifsc: str


@dataclass
class SplitAccount(Account):
    """Individual settlement split instruction."""

    amount_value: int


@dataclass
class SettlementSplits:
    """Settlement split instruction for bill."""

    parts: List[SplitAccount]
    primary_account: Account


@dataclass
class AmountValidationRule:
    """Amount validation rules, needed when amount_exactness is `RANGE`."""

    minimum: int
    maximum: int


@dataclass
class ValidationRules:
    """Validation rules for bill."""

    amount_validation: Optional[AmountValidationRule] = None
    source_accounts: Optional[List[Account]] = None


@dataclass
class MockCreditResponseData:
    """Mock Credit response."""

    utr: str


@dataclass
class RefundRequestItem:
    """Refund request item."""

    identifier: str
    identifierType: str
    refundType: str
    refundAmount: Optional[int] = None
    deductions: Optional[List[SplitAccount]] = None


@dataclass
class Deduction:
    """Deduction detail."""

    account: Account
    split: Amount


@dataclass
class RefundResponseItem:
    """Refund response item."""

    id: str
    bill_id: str
    transaction_ref_id: str
    amount: Amount
    status: str
    deductions: Optional[List[Deduction]] = None
    initiated_at: Optional[datetime] = None


@dataclass
class InitiateBatchRefundResponse:
    """Initiate Batch Refund Response."""

    batch_id: str
    refunds: List[Union[RefundResponseItem, SetuErrorResponseData]]


@dataclass
class BatchRefundStatusResponse:
    """Batch Refund Status Response."""

    batch_id: str
    refunds: List[RefundResponseItem]
