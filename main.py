from fastapi import FastAPI 
from crypt_name import Pseudonymize

pseudo = Pseudonymize()
pseudo.setup()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.post("/customer/{customer_name}")
async def post_customer(customer_name: str, customer_surname: str, customer_address: str, customer_postal: int, customer_city: str):
    customer_name = pseudo.pseudonymize(customer_name)
    
    return {
        "customer_name": customer_name,
        "customer_surname": customer_surname,
        "customer_address": customer_address,
        "customer_postal": customer_postal,
        "customer_city": customer_city
    }

@app.get("/users")
async def users():
    return ["Max", "Morty"]
