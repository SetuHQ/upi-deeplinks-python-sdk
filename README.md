# Setu

SDK to help Pythonistas integrate with Setu's APIs

Currently the following APIs are supported.

-   UPI DeepLinks

We're constantly adding new API support. Feel free to reach out to us if you
can't see any API.

## Installation

```bash
pip install setu
```

## Usage

### UPI DeepLinks

The following actions are currently supported

-   Generate payment link
-   Check status of payment link

#### Generate Link

```python
from setu import deeplink

dl = deeplink.Deeplink(
    "YOUR SCHEME ID",
    "YOUR JWT SECRET",
    "YOUR PRODUCT INSTANCE ID",
)
link = dl.generate_link(2300, 4, "gb", "1231243")
print(link["paymentLink"], link["platformBillID"])
```

#### Generate Link

```python
from setu import deeplink

status = dl.check_status(link['platformBillID'])
print(status["status"])
```

## License

MIT
