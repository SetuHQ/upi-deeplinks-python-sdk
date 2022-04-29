import requests
from auth import generate_setu_headers, AUTHTYPEJWT, AUTHTYPEOAUTH
from common import (
    URLS,
    MODEPRODUCTION,
    MODESANDBOX,
    URLADDCREDITPATH,
    URLBATCHREFUNDPATH,
    URLMOCKSETTLEMENTPATH,
    URLPAYMENTLINKPATH,
    URLREFUNDPATH,
)
from errors import handle_setu_errors


class Deeplink:
    def __init__(
        self, schemeId, secret, productInstance, authType=AUTHTYPEJWT, mode=MODESANDBOX
    ):
        self.schemeId = schemeId
        self.secret = secret
        self.productInstance = productInstance
        if mode == MODEPRODUCTION:
            self.url = URLS.Prod.url
        elif mode == MODESANDBOX:
            self.url = URLS.Sandbox.url
        else:
            # self.url = URLS.Local.url
            raise Exception("Invalid mode")
        self.mode = mode
        self.authType = authType

        if self.authType == AUTHTYPEOAUTH:
            # Generate required headers
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            # Set the url to v2
            self.url = self.url + "/v2"

    # Generate UPI payment link method
    def create_payment_link(self, payload):
        # In case of JWT the token expires often enough to warrant creation of new tokens
        if self.authType == AUTHTYPEJWT:
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )

        # Call API with required parameters
        response = requests.post(
            self.url + URLPAYMENTLINKPATH,
            data=payload.toJSON(),
            headers=self.headers,
        )

        if response.status_code == 401 or response.status_code == 403:
            generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            response = requests.post(
                self.url + URLPAYMENTLINKPATH,
                data=payload.toJSON(),
                headers=self.headers,
            )

        # Handle errors
        handle_setu_errors(response)

        return response.json()

    # Check status of UPI payment link method
    def check_payment_status(self, platformBillID):
        path = "{}/{}".format(URLPAYMENTLINKPATH, platformBillID)

        # In case of JWT the token expires often enough to warrant creation of new tokens
        if self.authType == AUTHTYPEJWT:
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )

        # Call API with required parameters
        response = requests.get(self.url + path, headers=self.headers)

        if response.status_code == 401 or response.status_code == 403:
            generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            response = requests.get(self.url + path, headers=self.headers)

        return response.json()

    # AVAILABLE ONLY FOR SANDBOX
    # Trigger mock payment for UPI payment link
    def trigger_mock_payment(self, amountValue, upiID):
        if self.mode == MODEPRODUCTION:
            raise Exception(
                "trigger_mock_payment METHOD IS IS NOT AVAILABLE IN PRODUCTION"
            )

        payload = {
            "amount": amountValue,
            "sourceAccount": {"accountID": "customer@vpa"},
            "destinationAccount": {"accountID": upiID},
            "type": "UPI",
        }

        # In case of JWT the token expires often enough to warrant creation of new tokens
        if self.authType == AUTHTYPEJWT:
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )

        # Call API with required parameters
        response = requests.post(
            self.url + URLADDCREDITPATH, json=payload, headers=self.headers
        )

        if response.status_code == 401 or response.status_code == 403:
            generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            response = requests.post(
                self.url + URLADDCREDITPATH, json=payload, headers=self.headers
            )

        return response.json()

    def initiate_batch_refund(self, refunds):
        # In case of JWT the token expires often enough to warrant creation of new tokens
        if self.authType == AUTHTYPEJWT:
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )

        # Call API with required parameters
        response = requests.post(
            self.url + URLBATCHREFUNDPATH,
            data=refunds.toJSON(),
            headers=self.headers,
        )

        if response.status_code == 401 or response.status_code == 403:
            generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            response = requests.post(
                self.url + URLBATCHREFUNDPATH,
                data=refunds.toJSON(),
                headers=self.headers,
            )

        # Handle errors
        handle_setu_errors(response)

        return response.json()

    def get_batch_refund_status(self, batch_refund_id):
        # In case of JWT the token expires often enough to warrant creation of new tokens
        if self.authType == AUTHTYPEJWT:
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )

        # Call API with required parameters
        response = requests.get(
            self.url + URLBATCHREFUNDPATH + "/" + batch_refund_id,
            headers=self.headers,
        )

        if response.status_code == 401 or response.status_code == 403:
            generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            response = requests.get(
                self.url + URLBATCHREFUNDPATH + "/" + batch_refund_id,
                headers=self.headers,
            )

        # Handle errors
        handle_setu_errors(response)

        return response.json()

    def get_refund_status(self, refund_id):
        # In case of JWT the token expires often enough to warrant creation of new tokens
        if self.authType == AUTHTYPEJWT:
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )

        # Call API with required parameters
        response = requests.get(
            self.url + URLREFUNDPATH + "/" + refund_id,
            headers=self.headers,
        )

        if response.status_code == 401 or response.status_code == 403:
            generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            response = requests.get(
                self.url + URLREFUNDPATH + "/" + refund_id,
                headers=self.headers,
            )

        # Handle errors
        handle_setu_errors(response)

        return response.json()

    def trigger_mock_settlement(self, utrs):
        payload = {
            "transactions": [],
        }

        for utr in utrs:
            payload["transactions"].append({"utr": utr})

        # In case of JWT the token expires often enough to warrant creation of new tokens
        if self.authType == AUTHTYPEJWT:
            self.headers = generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )

        # Call API with required parameters
        response = requests.post(
            self.url + URLMOCKSETTLEMENTPATH, json=payload, headers=self.headers
        )

        if response.status_code == 401 or response.status_code == 403:
            generate_setu_headers(
                self.schemeId,
                self.secret,
                self.productInstance,
                self.url,
                self.authType,
            )
            response = requests.post(
                self.url + URLMOCKSETTLEMENTPATH, json=payload, headers=self.headers
            )

        # Handle errors
        handle_setu_errors(response)

        return response.json()
