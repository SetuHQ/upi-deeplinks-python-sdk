# Setu 
This package helps you work with Setu's deeplink APIs.
* To generate a payment link
* To check status of the payment link

## Usage
```
    from setu import deeplink
    
    dl = deeplink.Deeplink(
        "262c5ab6-60d9-464e-a584-af008a8d0437", // SchemeId
        "e056f034-9da3-47e6-ba84-6cd16ccce6a3", // Secret
        "378992706761786990", // Product instance ID
    )
    link = dl.generate_link(2300, 4, "gb", "1231243")
    print(link["paymentLink"], link["platformBillID"])
    status = dl.check_status(link['platformBillID'])
    print(status["status"]) 
``` 