from fastapi import Depends,Response, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, Schema,models, utils, Oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=Schema.Token)
def log_in(user_cridentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # print(user_cridentials)
    user = db.query(models.User).filter(models.User.EMAIL == user_cridentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Cridentials")
    else:
        if not utils.verify_password(user_cridentials.password, user.PASSWORD):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Cridentials")
        else:
            access_token = Oauth2.create_access_token(data = {"user_id":user.ID, "user_email": user.EMAIL })
            return {"ACCESS_TOKEN": access_token, "TOKEN_TYPE": "bearer"}
