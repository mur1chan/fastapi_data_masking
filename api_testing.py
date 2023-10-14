import requests
r = requests

test = r.get("http://127.0.0.1:8000/customers/1")
print(f"Status code: {test.status_code}")
print(f"response: {test.json()}")
