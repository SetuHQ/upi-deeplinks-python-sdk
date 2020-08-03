# Setu 
This package helps you work with Setu's deeplink APIs.
* To generate a payment link
* To check status of the payment link

## Usage
```
    from setu import deeplink
    
    dl = deeplink.Deeplink(
        "random-uuid-here", // SchemeId
        "another-uuid-here", // Secret
        "123123123123123", // Product instance ID
    )
    link = dl.generate_link(2300, 4, "gb", "1231243")
    print(link["paymentLink"], link["platformBillID"])
    status = dl.check_status(link['platformBillID'])
    print(status["status"]) 
``` 