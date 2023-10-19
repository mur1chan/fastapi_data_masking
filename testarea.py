import requests

from database import Database


def post_customers():
    url = "http://localhost:8000/customer/Max"
    customer_name = "Max"
    customer_surname = "Mustermann"
    customer_address = "Musterstraße 123"
    customer_postal = 12345
    customer_city = "Musterstadt"

    data = {
        "customer_name": str(customer_name),
        "customer_surname": str(customer_surname),
        "customer_address": str(customer_address),
        "customer_postal": customer_postal,
        "customer_city": str(customer_city),
    }

    response = requests.post(url, params=data)

    if response.status_code == 200:
        print("Erfolgreich gesendet!")
        print(response.text)
    else:
        print("Fehler beim Senden:", response.status_code, response.text)


def post_create_database():
    url = "http://localhost:8000/create_db/somerandomstrings"
    response = requests.post(url)
    print(response.text)


def db_display_entries():
    db = Database("database_api.db", "customers")
    db.display_data()


if __name__ == "__main__":
    choice = int(
        input(
            "Create Database: 1\nPost customers:  2\nShow customer entries: 3\n[1, 2, 3]: "
        )
    )
    if choice == 1:
        post_create_database()
    elif choice == 2:
        post_customers()
    elif choice == 3:
        db_display_entries()
    else:
        print("wrong input")