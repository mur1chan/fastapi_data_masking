import requests
r = requests

test = r.post("http://127.0.0.1:8000/customers/moritz")
print(f"Status code: {test.status_code}")
print(f"response: {test.json()}")
