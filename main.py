from fastapi import FastAPI 
from crypt_name import Pseudonymize

pseudo = Pseudonymize()
pseudo.setup()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.post("/customers/{customer_name}")
async def get_customers(customer_name: str):
    customer_name = pseudo.pseudonymize(customer_name)
    return {"customer_name": customer_name}

@app.get("/users")
async def users():
    return ["Max", "Morty"]
