
from sqlite3 import IntegrityError
from ..database import get_db
from .. import models, Schema,utils
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/sqlalchemy/users",
    tags=["USERS"]
)
# CREATE USER
@router.post("/", status_code = status.HTTP_201_CREATED,response_model=Schema.User_Create_Response)
def create_user(user: Schema.User_Create,db: Session = Depends(get_db)):

    # PASSWORD HASSING
    try:
        hashed_password = utils.hash_pass(user.PASSWORD)
        user.PASSWORD = hashed_password

        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        print("----------------")
        print(IntegrityError)



# GET INDIVIDUAL USER BY ID
@router.get("/{id}",response_model=Schema.User_Create_Response)
def get_user(id: str,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.ID == str(id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with id " + str(id) + " not found")
    else:
        return user
