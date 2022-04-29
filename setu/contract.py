import json


class Account:
    def __init__(self, id, ifsc):
        self.id = id
        self.ifsc = ifsc


class Amount:
    def __init__(self, currency_code, value):
        self.currency_code = currency_code
        self.value = value


class Split:
    def __init__(self, unit, value):
        self.unit = unit
        self.value = value


class Part:
    def __init__(self, account, split):
        self.account = account
        self.split = split


class Settlement:
    def __init__(self, parts, primary_account, split):
        self.parts = parts
        self.primary_account = primary_account
        self.split = split


class SourceAccount:
    def __init__(self, number, ifsc):
        self.number = number
        self.ifsc = ifsc


class ValidationRules:
    def __init__(self, source_accounts):
        self.source_accounts = source_accounts


class Deduction:
    def __init__(self, account, split):
        self.account = account
        self.split = split


class RefundAmount:
    def __init__(self, currency_code, value):
        self.currencyCode = currency_code
        self.value = value


class PaymentLinkPayload:
    def __init__(
        self,
        amount,
        amount_exactness,
        biller_bill_id,
        additional_info=None,
        campaign_id=None,
        due_date=None,
        expiry_date=None,
        name=None,
        settlement=None,
        transaction_note=None,
        validation_rules=None,
    ):
        self.amount = amount
        self.amountExactness = amount_exactness
        self.billerBillID = biller_bill_id
        if additional_info:
            self.additionalInfo = additional_info
        if campaign_id:
            self.campaignID = campaign_id
        if due_date:
            self.dueDate = due_date
        if expiry_date:
            self.expiryDate = expiry_date
        if name:
            self.name = name
        if settlement:
            self.settlement = settlement
        if transaction_note:
            self.transactionNote = transaction_note
        if validation_rules:
            self.validationRules = validation_rules

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


class Refund:
    def __init__(
        self,
        seq_no,
        identifier,
        identifier_type,
        refund_type,
        refund_amount,
        deductions,
    ):
        self.seqNo = seq_no
        self.identifier = identifier
        self.identifierType = identifier_type
        self.refundType = refund_type
        self.refundAmount = refund_amount
        self.deductions = deductions


class BatchRefundPayload:
    def __init__(self, refunds):
        self.refunds = refunds

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
