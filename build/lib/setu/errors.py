def handle_setu_errors(response):
    if response.status_code == 500:
        raise Exception("Failed to get payment link", response.text)
    data = response.json()
    if not data["success"]:
        raise Exception("Bad credentials", data["error"])
