# Setu

SDK to help Pythonistas integrate with Setu's APIs

Currently the following APIs are supported.

-   UPI DeepLinks

We're constantly adding new API support. Feel free to reach out to us if you
can't see an API.

## Installation

```bash
pip install setu
```

## Usage

### UPI DeepLinks

The following actions are currently supported

-   Generate payment link
-   Check status of payment link

#### Configuration

```python
from setu import deeplink

dl = deeplink.Deeplink(
    "YOUR SCHEME ID",
    "YOUR JWT SECRET",
    "YOUR PRODUCT INSTANCE ID",
    mode="PRODUCTION | SANDBOX" # default SANDBOX,
    authType= "JWT | OAUTH" # default JWT
)
```

#### Generate UPI payment link

```python
link = dl.create_payment_link(
        amountValue=Number,
        billerBillID=String,
        amountExactness=String,
        dueDate=String, # Optional
        payeeName=String, # Optional
        expiryDate=String, # Optional
        settlement=Object, # Optional
        validationRules=Object, # Optional
        additionalInfo=Object # Optional
    )
print(link)
```

#### Check status of UPI payment link

```python
status = dl.check_payment_status(
        platformBillID=String
    )
print(status)
```

#### Trigger mock payment for UPI payment link - ONLY IN SANDBOX ⚠️

```python
status = dl.trigger_mock_payment(
        amountValue=Number, # Decimal Value
        upiID=String # UPI ID generated by create_payment_link method
    )
print(status)
```

## License

MIT
