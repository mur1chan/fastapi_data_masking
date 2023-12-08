from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.auth import Authorization
from app.crypt_name import Pseudonymize
from app.database import Database

pseudo = Pseudonymize()
auth = Authorization()
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