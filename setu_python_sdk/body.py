"""Body builder helper module."""
from typing import Any, Dict, List, cast

from setu_python_sdk.contract import RefundRequestItem


def get_create_payment_link_body(**kwargs) -> Dict[str, Any]:
    """Get the payload for Create Payment Link API."""
    payload: Dict[str, Any] = {
        "amount": {"currencyCode": "INR", "value": kwargs['amount_value']},
        "amountExactness": kwargs['amount_exactness'],
        "billerBillID": kwargs['biller_bill_id'],
    }

    if kwargs['payee_name'] is not None:
        payload.update({"name": kwargs['payee_name']})

    if kwargs['transaction_note'] is not None:
        payload.update({"transactionNote": kwargs['transaction_note']})

    if kwargs['expiry_date'] is not None:
        expiry_date_str = kwargs['expiry_date'].replace(microsecond=0).isoformat() + "Z"
        payload.update({"expiryDate": expiry_date_str})

    if kwargs['settlement'] is not None:
        payload.update(
            {
                "settlement": {
                    "parts": [
                        {
                            "account": {
                                "id": part.account_number,
                                "ifsc": part.account_ifsc,
                            },
                            "split": {
                                "unit": "INR",
                                "value": part.amount_value,
                            },
                        }
                        for part in kwargs['settlement'].parts
                    ],
                    "primaryAccount": {
                        "id": kwargs['settlement'].primary_account.account_number,
                        "ifsc": kwargs['settlement'].primary_account.account_ifsc,
                    },
                }
            }
        )

    if kwargs['validation_rules'] is not None:
        vr: Dict[str, Any] = {}
        if kwargs['validation_rules'].amount_validation is not None:
            vr.update(
                {
                    "amount": {
                        "maximum": kwargs['validation_rules'].amount_validation.maximum,
                        "minimum": kwargs['validation_rules'].amount_validation.minimum,
                    }
                }
            )
        if kwargs['validation_rules'].source_accounts is not None:
            vr.update(
                {
                    "sourceAccounts": [
                        {"number": source_account.account_number, "ifsc": source_account.account_ifsc}
                        for source_account in kwargs['validation_rules'].source_accounts
                    ]
                }
            )
        payload.update({"validationRules": vr})

    if kwargs['additional_info'] is not None:
        payload.update({"additionalInfo": kwargs['additional_info']})

    if kwargs['campaign_id'] is not None:
        payload.update({"campaignID": kwargs['campaign_id']})

    return payload


def get_mock_credit_body(**kwargs) -> Dict[str, Any]:
    """Get the payload for Mock Credit API."""
    payload = {
        "amount": kwargs['amount_value'],
        "type": "UPI",
        "sourceAccount": {"accountID": "customer@vpa"},
        "destinationAccount": {"accountID": kwargs['upi_id']},
        "transactionReference": kwargs["platform_bill_id"],
    }

    return payload


def get_mock_settlement_body(**kwargs) -> Dict[str, Any]:
    """Get the payload for Mock Settlement API."""
    transactions = [{"utr": utr} for utr in kwargs['utrs']]
    payload = {"transactions": transactions}

    return payload


def get_batch_refund_body(**kwargs) -> Dict[str, Any]:
    """Get the payload for Initiate Batch Refund API."""
    payload = {
        "refunds": [
            {
                "seqNo": i,
                "identifier": refund.identifier,
                "identifierType": refund.identifierType,
                "refundType": refund.refundType,
                "refundAmount": refund.refundAmount,
                "deductions": [
                    {
                        "account": {"id": deduction.account_number, "ifsc": deduction.account_ifsc},
                        "split": {"value": deduction.amount_value, "unit": "INR"},
                    }
                    for deduction in (refund.deductions if refund.deductions is not None else [])
                ],
            }
            for i, refund in enumerate(cast(List[RefundRequestItem], kwargs['refunds']))
        ],
    }

    return payload
