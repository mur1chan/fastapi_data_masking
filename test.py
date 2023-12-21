import requests

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzAyMTUwNTI5fQ.ssuD38epNrT7YlzHCKNEkd_c7kCMJhlHvmZz7O0O8iM',
    'Content-Type': 'application/json',
}

json_data = {
    'values': [
        'string',
        'test',
        123,
    ],
    'salt': 'string',
}

response = requests.post('http://localhost/pseudonymize', headers=headers, json=json_data)
print(response.text)