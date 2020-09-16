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

    def __init__(self, schemeId, secret, productInstance, production=False):
        self.schemeId = schemeId
        self.secret = secret
        self.productInstance = productInstance
        self.url = URLS.Sandbox.url if not production else URLS.Prod.url

    def createPaymentLink(
        self,
        amountValue,
        billerBillID,
        amountExactness,
        dueDate,
        expiryDate,
        payeeName,
        settlement,
        validationRules
    ):

        path = "/payment-links"
        payload = {
            "amount": {
                "currencyCode": "INR",
                "value": amountValue
            },
            "amountExactness": amountExactness,
            "billerBillID": billerBillID,
            "name": payeeName,
            "dueDate": dueDate,
            "expiryDate": expiryDate
        }

        if settlement:
            payload.update({"settlement": settlement})

        if validationRules:
            payload.update({"validationRules": validationRules})

        if amountExactness == "EXACT_UP":
            payload["validationRules"] = {
                "amount": {
                    "maximum": 0,
                    "minimum": amountValue
                }
            }
        elif amountExactness == "EXACT_DOWN":
            payload["validationRules"] = {
                "amount": {
                    "maximum": amountValue,
                    "minimum": 0
                }
            }

        headers = generate_setu_headers(
            self.schemeId, self.secret, self.productInstance
        )
        response = requests.post(
            self.url + path, json=payload, headers=headers
        )
        handle_setu_errors(response)
        data = response.json()
        self.platformBillID = data["data"]["platformBillID"]
        return data["data"]

    def checkPaymentStatus(self, platformBillID=None):
        bill_id = self.platformBillID
        if platformBillID:
            bill_id = platformBillID
        path = "/payment-links/{}".format(bill_id)
        headers = generate_setu_headers(
            self.schemeId, self.secret, self.productInstance
        )
        response = requests.get(
            self.url + path, headers=headers
        )
        data = response.json()
        print(data)
        return data["data"]

    def mock_payment(self, amountValue, upiId):
        path = "/triggers/funds/addCredit"
        payload = {
            "amount": amountValue,
            "destinationAccount": {
                "accountID": upiId
            },
            "sourceAccount": {
                "accountID": "customer@vpa"
            },
            "type": "UPI",
        }

        headers = generate_setu_headers(
            self.schemeId, self.secret, self.productInstance
        )
        response = requests.post(
            self.url + path, json=payload, headers=headers
        )
        if response.status_code != 200:
            raise Exception("Failed to mock payment", )
        return "Mock success"
