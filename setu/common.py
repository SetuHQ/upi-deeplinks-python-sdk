URLADDCREDITPATH = "/triggers/funds/addCredit"
URLBATCHREFUNDPATH = "/refund/batch"
URLMOCKSETTLEMENTPATH = "/triggers/funds/mockSettlement"
URLPAYMENTLINKPATH = "/payment-links"
URLREFUNDPATH = "/refund"

# MODELOCAL = "LOCAL"
MODEPRODUCTION = "PRODUCTION"
# MODEQA = "QA"
MODESANDBOX = "SANDBOX"


class URLS:
    # class Local:
    #     url = "http://localhost:8080/api"

    class Prod:
        url = "https://prod.setu.co/api"

    # class QA:
    #     url = "https://api-blue-qa.setu.co/api"

    class Sandbox:
        url = "https://uat.setu.co/api"
