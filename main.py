from fastapi import FastAPI 


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.get("/customers/{customers_id}")
async def get_customers(customers_id: int):
    return {"customers_id": customers_id}

@app.get("/users")
async def users():
    return ["Max", "Morty"]
