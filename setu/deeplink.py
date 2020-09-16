import requests
import datetime
from .auth import generate_setu_headers
from .errors import handle_setu_errors


class URLS:

    class Sandbox:
        url = "https://sandbox.setu.co/api"

    class Prod:
        url = "https://prod.setu.co/api"


class Deeplink:

    def __init__(self, schemeId, secret, productInstance, mode="SANDBOX"):
        self.schemeId = schemeId
        self.secret = secret
        self.productInstance = productInstance
        self.url = URLS.Sandbox.url if mode != "PRODUCTION" else URLS.Prod.url
        self.mode = mode

    # Generate UPI payment link method
    def create_payment_link(
        self,
        amountValue,
        billerBillID,
        amountExactness,
        dueDate=None,
        expiryDate=None,
        payeeName=None,
        settlement=None,
        validationRules=None
    ):

        path = "/payment-links"
        payload = {
            "amount": {
                "currencyCode": "INR",
                "value": amountValue
            },
            "amountExactness": amountExactness,
            "billerBillID": billerBillID
        }

        if payeeName is not None:
            payload.update({"name": payeeName})

        if dueDate is not None:
            payload.update({"dueDate": dueDate})

        if expiryDate is not None:
            payload.update({"expiryDate": expiryDate})

        if settlement is not None:
            payload.update({"settlement": settlement})

        if validationRules is not None:
            payload.update({"validationRules": validationRules})

        # Generate required headers
        headers = generate_setu_headers(
            self.schemeId, self.secret, self.productInstance
        )

        # Call API with required parameters
        response = requests.post(
            self.url + path, json=payload, headers=headers
        )

        # Handle errors
        handle_setu_errors(response)

        return response.json()

    # Check status of UPI payment link method
    def check_payment_status(
        self,
        platformBillID
    ):
        path = "/payment-links/{}".format(platformBillID)

        # Generate required headers
        headers = generate_setu_headers(
            self.schemeId, self.secret, self.productInstance
        )

        # Call API with required parameters
        response = requests.get(
            self.url + path, headers=headers
        )

        return response.json()

    # AVAILABLE ONLY FOR SANDBOX
    # Trigger mock payment for UPI payment link
    def trigger_mock_payment(self, amountValue, upiID):

        if self.mode == "PRODUCTION":
            raise Exception(
                "trigger_mock_payment METHOD IS IS NOT AVAILABLE IN PRODUCTION"
            )

        path = "/triggers/funds/addCredit"
        payload = {
            "amount": amountValue,
            "destinationAccount": {
                "accountID": upiID
            },
            "sourceAccount": {
                "accountID": "customer@vpa"
            },
            "type": "UPI",
        }

        # Generate required headers
        headers = generate_setu_headers(
            self.schemeId, self.secret, self.productInstance
        )

        # Call API with required parameters
        response = requests.post(
            self.url + path, json=payload, headers=headers
        )

        return response
