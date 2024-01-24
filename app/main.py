import hashlib
import os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from app.auth import Authorization
from app.pseudo import Pseudonymize

pseudo = Pseudonymize()
auth = Authorization()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

class Anonymize(BaseModel):
    values: list[str]


password = os.getenv("PASSWORD")

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"


class Pseudonymize(BaseModel):
    values: list[str]
    password: str

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
        token_data = auth.get_user(password)
    except JWTError:
        raise credentials_exception
    user = auth.get_user(password, username=token_data["username"])
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login_for_access_token(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    OAuth2 compatible token login endpoint used to obtain a new access token. This endpoint
    authenticates the user using the username and password provided in the request body.

    - **username**: The username of the user.
    - **password**: The password of the user.
    """
    user = auth.authenticate_user(password, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token = auth.create_access_token(data={"sub": user})
        return {"access_token": access_token, "token_type": "bearer"}


@app.post("/pseudonymize")
async def pseudonymize(
    pseudonymize: Pseudonymize, current_user: Annotated[str, Depends(get_current_user)]
):
    """
    Endpoint for pseudonymizing a list of values. It uses a specified password to pseudonymize
    each value in the list. The user must be authenticated to access this endpoint.

    - **values**: A list of values to be pseudonymized.
    - **password**: A password used for the pseudonymization process.
    """
    response = []
    for value in pseudonymize.values:
        response.append(pseudo.pseudo(str(value), pseudonymize.password))

    return {"values": response}


@app.post("/unpseudonymize")
async def unpseudonymize(
    pseudonymize: Pseudonymize, current_user: Annotated[str, Depends(get_current_user)]
):
    """
    Endpoint for unpseudonymizing a list of previously pseudonymized values. This process
    requires the same password that was used for pseudonymization. User authentication is required.

    - **values**: A list of pseudonymized values to be reverted to their original form.
    - **password**: The password used during the original pseudonymization process.
    """
    response = []
    for value in pseudonymize.values:
        response.append(pseudo.unpseudo(value, pseudonymize.password))

    return {"values": response}


@app.post("/anonymize")
async def anonymize(
    anonymize: Anonymize, current_user: Annotated[str, Depends(get_current_user)]
):
    """
    Endpoint for anonymizing a list of values. Anonymization is a process of data transformation
    where the values are turned into non-reversible hashes. This is often used for enhancing data privacy.
    User authentication is required to access this endpoint.

    - **values**: A list of values to be anonymized.
    """
    response = []

    for value in anonymize.values:
        hash_object = hashlib.sha256()

        hash_object.update(value.encode())

        hashed_value = hash_object.hexdigest()

        response.append(hashed_value)

    return {"values": response}
