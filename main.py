from fastapi import FastAPI

from crypt_name import Pseudonymize
from database import Database

pseudo = Pseudonymize()
pseudo.setup()
db = Database("database_api.db", "customers")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.post("/create_db/somerandomstrings")
async def create_db():
    create_db = db.create_database()
    if create_db is True:
        return {"success": "the database was successfully created"}
    else:
        return {"error": "please check the API logs"}
    # TODO: add key for verification (API KEY or berear token)


@app.post("/customer/{customer_name}")
async def post_customer(
    customer_name: str,
    customer_surname: str,
    customer_address: str,
    customer_postal: int,
    customer_city: str,
):
    customer_name = pseudo.pseudonymize(customer_name)
    customer_surname = pseudo.pseudonymize(customer_surname)
    customer_address = pseudo.pseudonymize(customer_address)
    customer_city = pseudo.pseudonymize(customer_city)
    customer_insert = db.insert_data(
        str(customer_name),
        str(customer_surname),
        str(customer_address),
        customer_postal,
        str(customer_city),
    )

    if customer_insert is True:
        return {
            "customer_name": customer_name,
            "customer_surname": customer_surname,
            "customer_address": customer_address,
            "customer_postal": customer_postal,
            "customer_city": customer_city,
        }
    else:
        return {"failed": "error"}


@app.delete("/customer/{customer_name}")
async def delete_customer(customer_name: str):
    customer_name_pseudonymized = pseudo.pseudonymize(customer_name)
    deletion_status = db.delete_row_by_name(customer_name_pseudonymized)

    if deletion_status:
        return {"success": f"Customer {customer_name} was successfully deleted"}
    else:
        return {"error": f"Failed to delete customer {customer_name}."}


@app.put("/customer/{customer_name}")
async def update_customer(
    customer_name: str,
    new_customer_name: str = None,
    new_customer_surname: str = None,
    new_customer_address: str = None,
    new_customer_postal: int = None,
    new_customer_city: str = None,
):
    customer_name_pseudonymized = pseudo.pseudonymize(customer_name)

    new_customer_name = pseudo.pseudonymize(new_customer_name) if new_customer_name else None
    new_customer_surname = pseudo.pseudonymize(new_customer_surname) if new_customer_surname else None
    new_customer_address = pseudo.pseudonymize(new_customer_address) if new_customer_address else None
    new_customer_city = pseudo.pseudonymize(new_customer_city) if new_customer_city else None

    update_status = db.update_data_by_name(
        customer_name_pseudonymized,
        new_customer_name,
        new_customer_surname,
        new_customer_address,
        new_customer_postal,
        new_customer_city
    )

    if update_status:
        return {"success": f"Customer {customer_name}'s details were successfully updated"}
    else:
        return {"error": f"Failed to update details for customer {customer_name}."}

