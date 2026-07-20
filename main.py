from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from Project_2 import models, schemas

app = FastAPI()

@app.get("/")
def root():
    return {"message": "My name is Ahmad"}

@app.post("/items", status_code=status.HTTP_200_OK)
def add_item(item: schemas.Item, db: Session = Depends(get_db)):
    new_item = models.Item(**item.dict())

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    query = db.query(models.Item).all()

    return {"data": query}

@app.get("/items")
def get_item(db: Session = Depends(get_db)):
    query = db.query(models.Item).all()

    return {"data": query}

# @app.put("/items/{id}")
# def update_item(id: int, db: Session = Depends(get_db)):
#     query = db.query(models.Item).filter(models.Item.id == id).first()
 
#     if query is None: