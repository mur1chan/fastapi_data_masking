import requests

# Definieren Sie die URL des Endpunkts und ersetzen Sie {customer_name} durch den gewünschten Kundenname.
url = "http://localhost:8000/customer/Max"

# Ersetzen Sie die Platzhalterwerte durch die tatsächlichen Werte, die Sie senden möchten.
customer_name = "Max"
customer_surname = "Mustermann"
customer_address = "Musterstraße 123"
customer_postal = 12345
customer_city = "Musterstadt"

# Erstellen Sie ein Dictionary mit den Daten, die Sie senden möchten.
data = {
    "customer_name": customer_name,
    "customer_surname": customer_surname,
    "customer_address": customer_address,
    "customer_postal": customer_postal,
    "customer_city": customer_city
}

# Führen Sie die POST-Anfrage aus.
response = requests.post(url, params=data)

# Überprüfen Sie die Antwort.
if response.status_code == 200:
    print("Erfolgreich gesendet!")
    print(response.text)
else:
    print("Fehler beim Senden:", response.status_code, response.text)
