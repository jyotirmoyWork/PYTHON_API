from typing import Optional
from pydantic import BaseModel, EmailStr, conint

from app.models import Post_Two






class User_Create(BaseModel):
    EMAIL: EmailStr
    PASSWORD: str


class User_Create_Response(BaseModel):
    ID: str
    EMAIL: EmailStr
    # PASSWORD: str
    class Config:
        orm_mode= True


class User_login(BaseModel):
    EMAIL: EmailStr
    PASSWORD: str

class Token(BaseModel):
    ACCESS_TOKEN: str
    TOKEN_TYPE: str

class Token_data(BaseModel):
    ID: Optional[str] = None
    EMAIL: EmailStr

# class Oauth_user_details(BaseModel):
#     user_id: int
#     user_email: str


class Posts(BaseModel):
    TITLE: str
    CONTENT: str
    PUBLISHED: bool = True
    OWNER: User_Create_Response


class Post_Base(BaseModel):
    TITLE: str
    CONTENT: str
    
    # PUBLISHED: bool = True

class Create_Post(Post_Base):
    pass


# class Post_Response(Post_Base):
#     ID: int
#     OWNER_ID: int
#     OWNER: User_Create_Response

#     class Config:
#         orm_mode= True


# "Post_Two": {
#             "ID": 4,
#             "PUBLISHED": true,
#             "OWNER_ID": 1,
#             "CONTENT": "Post 4 content",
#             "TITLE": "POst 4",
#             "CREATED_AT": "2022-01-31T23:13:23.639257+05:30"
#         },
#         "votes": 1

class Posts_ONE(Post_Base):
    ID: int
    TITLE: str
    CONTENT: str
    PUBLISHED: bool
    OWNER_ID: int
    OWNER: User_Create_Response
    
    class Config:
	    orm_mode=True
    
    

class Post_Response(BaseModel):
    Post_Two: Posts_ONE
    votes: int

    class Config:
        orm_mode= True
        
        
        

class vote(BaseModel):
    POST_ID: int
    DIR: conint(le=1)