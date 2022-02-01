
from pyexpat import model
from urllib import response

from sqlalchemy import func
from ..database import get_db
from .. import models, Schema, Oauth2
from fastapi import Depends, Response, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional


# PREFIX FOR BASE ROUTE
router = APIRouter(
    prefix="/sqlalchemy/posts",
    tags=["POSTS"]
)


# GET ALL POSTS
@router.get("/", response_model=List[Schema.Post_Response])
# @router.get("/")
def get_post(db: Session = Depends(get_db), user_data=Depends(Oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post_Two).filter(
    #     models.Post_Two.TITLE.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post_Two,func.count(models.Votes.POST_ID).label("votes")).join(models.Votes, models.Votes.POST_ID == models.Post_Two.ID, isouter=True).group_by(models.Post_Two.ID).filter(
        models.Post_Two.TITLE.contains(search)).limit(limit).offset(skip).all()
    print(results)
    # print(limit)
    return results


# # GET ALL POSTS FOR ONLY SPECIFIC USER
# @router.get("/",response_model=List[Schema.Post_Response])
# def test_post(db: Session = Depends(get_db), user_data = Depends(Oauth2.get_current_user)):
#     posts = db.query(models.Post_Two).filter(models.Post_Two.OWNER_ID == user_data.ID).all()
#     return  posts


# CREATE A SINGLE POST
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: Schema.Create_Post, db: Session = Depends(get_db), user_data=Depends(Oauth2.get_current_user)):
    try:
        print(user_data.EMAIL)
        # post.update({"OWNER_ID": user_data.ID})
        new_post = models.Post_Two(OWNER_ID=user_data.ID, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except:
        return "some err"


# GET SINGLE POST BY ID
@router.get("/{id}", response_model=Schema.Post_Response)
def get_post_one(id: int, db: Session = Depends(get_db), user_data=Depends(Oauth2.get_current_user)):
    print(user_data.EMAIL)
    post = db.query(models.Post_Two,func.count(models.Votes.POST_ID).label("votes")).join(models.Votes, models.Votes.POST_ID == models.Post_Two.ID, isouter=True).group_by(models.Post_Two.ID).filter(
        models.Post_Two.ID == str(id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id " + str(id) + " not found")
    return post


# # GET SINGLE POST BY ID FOR ONLY SPECIFIC USER
# @router.get("/{id}",response_model=Schema.Post_Response)
# def get_post_one(id:int, db: Session = Depends(get_db),user_data = Depends(Oauth2.get_current_user)):
#     print(user_data.EMAIL)
#     post = db.query(models.Post_Two).filter(models.Post_Two.ID == str(id)).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id " + str(id) + " not found")
#     if post.OWNER_ID != user_data.ID:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorizr to access this post with id " + str(id))
#     return post


# DELETE A SINGLE POST
@router.delete("/{id}", status_code=status.HTTP_201_CREATED)
def delete_post(id: int, db: Session = Depends(get_db), user_data=Depends(Oauth2.get_current_user)):
    print(user_data.ID)
    post_query = db.query(models.Post_Two).filter(
        models.Post_Two.ID == str(id))
    post = post_query.first()
    # print(post.OWNER_ID)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.OWNER_ID != user_data.ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorize for delete the post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE A SINGLE POST
@router.put("/{id}")
def update_post(id: int, updated_post: Schema.Create_Post, db: Session = Depends(get_db), user_data=Depends(Oauth2.get_current_user)):
    print(user_data.EMAIL)
    post_query = db.query(models.Post_Two).filter(
        models.Post_Two.ID == str(id))
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.OWNER_ID != user_data.ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorize for modify the post")
    else:
        post_query.update(updated_post.dict())
        db.commit()
        return post_query.first()
