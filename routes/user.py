from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, models
import hashing

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def create_user(user: schemas.User,  db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == user.email).first()

    if not (query is None):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"This email is alredy exists. Try another email")

    user.password = hashing.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user