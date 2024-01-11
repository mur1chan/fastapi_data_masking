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


class AnonymizeData(BaseModel):
    values: list[str]


kunden = {"test": {"hashed_password": os.getenv("PASSWORD")}}

SECRET_KEY = os.getenv("PASSWORD")
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
        token_data = auth.get_user(kunden, username)
    except JWTError:
        raise credentials_exception
    user = auth.get_user(kunden, username=token_data["username"])
    if user is None:
        raise credentials_exception
    return user


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


@app.post("/pseudonymize")
async def pseudonymize(
    pseudonymize: Pseudonymize, current_user: Annotated[str, Depends(get_current_user)]
):
    response = []
    for value in pseudonymize.values:
        response.append(pseudo.pseudo(str(value), pseudonymize.password))

    return {"values": response}


@app.post("/unpseudonymize")
async def unpseudonymize(
    pseudonymize: Pseudonymize, current_user: Annotated[str, Depends(get_current_user)]
):
    response = []
    for value in pseudonymize.values:
        response.append(pseudo.unpseudo(value, pseudonymize.password))

    return {"values": response}


@app.post("/anonymize")
async def anonymize(data: AnonymizeData, current_user: Annotated[str, Depends(get_current_user)]):
    response = []

    for value in data.values:
        hash_object = hashlib.sha256()

        hash_object.update(value.encode())

        hashed_value = hash_object.hexdigest()

        response.append(hashed_value)

    return {"values": response}
