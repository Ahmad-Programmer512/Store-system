from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from schemas import Item_Response, Item
from oauth2 import get_current_user
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
import models, schemas
import json

router = APIRouter(
    prefix="/api/products",
    tags=['Items']
)

# {"name":"apple","price":10,"category":"fruit","quantity":10}
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_item(item: str = Form(...), db: Session = Depends(get_db), current_user: int = Depends(get_current_user), file: UploadFile = File(...)):
    if current_user.email != "admin@gmail.com":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are not able to add items")
    product = schemas.Item.model_validate(json.loads(item))

    query = db.query(models.Item).filter(models.Item.name == product.name).first()

    if query is not None:
        query.quantity += product.quantity
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Item quantity has been increased.")

    with open(f"uploads/{file.filename}", "wb") as image:
        image.write(await file.read())

    product_dict = product.model_dump()
    product_dict["image_url"] = f"uploads/{file.filename}"
    
    new_item = models.Item(**product_dict)

    db.add(new_item)
    db.commit()
    db.refresh(new_item)


    return {
        "message": "Image added successfully.",
        "URL": f"uploads/{file.filename}"
    }


@router.get("/", response_model=list[Item_Response])
def get_items(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = db.query(models.Item).filter(models.Item.name.ilike(f"%{search}%"))

    items = (
        query.order_by(models.Item.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return items

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