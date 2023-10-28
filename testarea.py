import requests

from database import Database


def post_customers():
    url = "http://localhost:8000/customer/Max"
    customer_name = "Max"
    customer_surname = "Mustermann"
    customer_address = "Musterstraße 123"
    customer_postal = 12345
    customer_city = "Musterstadt"
    salt = "salt"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjk4NTkzMzM5fQ.WPaK0FglJpx5EPviAHJtzciH37QXd5_uvJjnKE4HZuI"
    }
    data = {
        "customer_name": str(customer_name),
        "customer_surname": str(customer_surname),
        "customer_address": str(customer_address),
        "customer_postal": customer_postal,
        "customer_city": str(customer_city),
        "salt": str(salt),
    }

    response = requests.post(url, params=data, headers=headers)

    if response.status_code == 200:
        print("Erfolgreich gesendet!")
        print(response.text)
    else:
        print("Fehler beim Senden:", response.status_code, response.text)


def post_create_database():
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjk4NTkzMzM5fQ.WPaK0FglJpx5EPviAHJtzciH37QXd5_uvJjnKE4HZuI"
    }

    url = "http://localhost:8000/create_db/somerandomstrings"
    response = requests.post(url, headers=headers)
    print(response.text)


def db_display_entries():
    db = Database("database_api.db", "customers")
    db.display_data()


def login():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "",
        "username": "test",
        "password": "secret",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    r = requests.post("http://127.0.0.1:8000/token", headers=headers, data=data)
    print(r.text)


if __name__ == "__main__":
    choice = int(
        input(
            "Create Database: 1\nPost customers:  2\nShow customer entries: 3\nLogin: 4\n[1, 2, 3, 4]: "
        )
    )
    if choice == 1:
        post_create_database()
    elif choice == 2:
        post_customers()
    elif choice == 3:
        db_display_entries()
    elif choice == 4:
        login()
    else:
        print("wrong input")
