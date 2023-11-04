from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from auth import Authorization
from crypt_name import Pseudonymize
from database import Database

pseudo = Pseudonymize()
auth = Authorization()
db = Database("database_api.db", "customers")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

kunden = {
    "test": {
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
}

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth.get_user(kunden, username)
    except JWTError:
        raise credentials_exception
    user = auth.get_user(kunden, username=token_data["username"])
    if user is None:
        raise credentials_exception
    return user


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.post("/token")
async def login_for_access_token(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = auth.authenticate_user(kunden, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token = auth.create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}


@app.post("/create_db/somerandomstrings")
async def create_db(current_user: Annotated[str, Depends(get_current_user)]):
    create_db = db.create_database()
    if create_db is True:
        return {"success": "the database was successfully created"}
    else:
        return {"error": "please check the API logs"}


@app.post("/customer/{customer_name}")
async def post_customer(
    customer_name: str,
    customer_surname: str,
    customer_address: str,
    customer_postal: int,
    customer_city: str,
    salt: str,
    current_user: Annotated[str, Depends(get_current_user)],
):
    customer_name = pseudo.pseudo_name(customer_name, salt)
    customer_surname = pseudo.pseudo_name(customer_surname, salt)
    customer_address = pseudo.pseudo_street(customer_address, salt)
    customer_postal = pseudo.pseudo_postal(customer_postal, salt)
    customer_city = pseudo.pseudo_city(customer_city, salt)
    # customer_insert = db.insert_data(
    #     str(customer_name),
    #     str(customer_surname),
    #     str(customer_address),
    #     customer_postal,
    #     str(customer_city),
    # )

    return {
        "customer_name": customer_name,
        "customer_surname": customer_surname,
        "customer_address": customer_address,
        "customer_postal": customer_postal,
        "customer_city": customer_city,
    }


# @app.delete("/customer/{customer_name}")
# async def delete_customer(customer_name: str, current_user: Annotated[str, Depends(get_current_user)]):
#     customer_name_pseudonymized = pseudo.pseudonymize(customer_name)
#     deletion_status = db.delete_row_by_name(customer_name_pseudonymized)
#
#     if deletion_status:
#         return {"success": f"Customer {customer_name} was successfully deleted"}
#     else:
#         return {"error": f"Failed to delete customer {customer_name}."}
#
#
# @app.put("/customer/{customer_name}")
# async def update_customer(
#     customer_name: str,
#     new_customer_name: str = None,
#     new_customer_surname: str = None,
#     new_customer_address: str = None,
#     new_customer_postal: int = None,
#     new_customer_city: str = None,
# ):
#     customer_name_pseudonymized = pseudo.pseudonymize(customer_name)
#
#     new_customer_name = pseudo.pseudonymize(new_customer_name) if new_customer_name else None
#     new_customer_surname = pseudo.pseudonymize(new_customer_surname) if new_customer_surname else None
#     new_customer_address = pseudo.pseudonymize(new_customer_address) if new_customer_address else None
#     new_customer_city = pseudo.pseudonymize(new_customer_city) if new_customer_city else None
#
#     update_status = db.update_data_by_name(
#         customer_name_pseudonymized,
#         new_customer_name,
#         new_customer_surname,
#         new_customer_address,
#         new_customer_postal,
#         new_customer_city
#     )
#
#     if update_status:
#         return {"success": f"Customer {customer_name}'s details were successfully updated"}
#     else:
#         return {"error": f"Failed to update details for customer {customer_name}."}
#
