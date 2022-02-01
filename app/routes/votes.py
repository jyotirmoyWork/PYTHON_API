from fastapi import Depends, Response, HTTPException, status, APIRouter
from .. import Schema, database, models, Oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote: Schema.vote, db: Session = Depends(database.get_db), current_user=Depends(Oauth2.get_current_user)):

    post = db.query(models.Post_Two).filter(
        models.Post_Two.ID == vote.POST_ID).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id { vote.POST_ID} not exists")
    vote_query = db.query(models.Votes).filter(
        models.Votes.POST_ID == vote.POST_ID, models.Votes.USER_ID == current_user.ID)
    found_vote = vote_query.first()
    if vote.DIR == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.ID} has already voted")
        new_vote = models.Votes(POST_ID=vote.POST_ID, USER_ID=current_user.ID)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added success!"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
