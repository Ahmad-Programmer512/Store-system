from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from schemas import Item_Response, Item
from oauth2 import get_current_user
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/items",
    tags=['Items']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_item(item: Item, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    if current_user.email != "admin@gmail.com":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are not able to add items")

    query = db.query(models.Item).filter(models.Item.name == item.name).first()

    if query is not None:
        query.quantity += item.quantity
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Item quantity has been increased.")

    new_item = models.Item(**item.dict())

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

@router.get("/", response_model=list[Item_Response])
def get_items(db: Session = Depends(get_db)):
    query = db.query(models.Item).all()

    return query

@router.get("/{id}", response_model=Item_Response)
def get_item(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Item).filter(models.Item.id == id).first()

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id: {id} was not found")

    return query

@router.put("/{id}", response_model=Item_Response)
def update_item(id: int, item: Item, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    if current_user.email != "admin@gmail.com":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are not able to add items")
    
    query = db.query(models.Item).filter(models.Item.id == id)

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id: {id} was not found")
    
    query.update(item.dict(), synchronize_session=False)

    db.commit()

    return query.first()