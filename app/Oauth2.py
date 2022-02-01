from jose import JWTError, jwt
from datetime import datetime, timedelta

from app import models
from . import Schema, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

print(settings.SECRECT_KEY)

Oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
# SECRECT KEY
SECRECT_KEY =settings.SECRECT_KEY
# ALGORITHM
ALGORITHM = settings.ALGORITHMS
# EXPIRATION
ACCESS_TOKEN_EXPIRATION_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTE


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token: str, cridential_exception):
    try:
        payload = jwt.decode(token, SECRECT_KEY, ALGORITHM)
        user_id = payload.get("user_id")
        user_email = payload.get("user_email")
       
        if not user_id or not user_email:
            # print(user_id)
            # print(user_email)
            raise cridential_exception
        token_data =Schema.Token_data(ID=user_id, EMAIL=user_email)
        
        # return token_data
    except JWTError:
        raise cridential_exception
    return token_data


def get_current_user(token: str = Depends(Oauth2_schema),db: Session = Depends(database.get_db)):
    cridential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate cridentials", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, cridential_exception)
    # print(token)
    user = db.query(models.User).filter(models.User.ID == token.ID).first()
    # print(user)
    return user