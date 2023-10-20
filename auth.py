from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

class Authorization:
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password):
        return pwd_context.hash(password)


    def get_user(self, db, username):
        if username in db:
            return {"username": username, "password":db[username]["hashed_password"]}


    def authenticate_user(self, db, username, password):
        user = self.get_user(db, username)
        if not user:
            return False
        if not self.verify_password(password, db[username]["hashed_password"]):
            return False
        return user


    def create_access_token(self, data):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=1440)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt