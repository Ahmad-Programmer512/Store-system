from fastapi import FastAPI, Depends, HTTPException, status
from schemas import Item_Response, Item
from sqlalchemy.orm import Session
from routes import item, user, auth, buying_item
from database import get_db
import models

app = FastAPI()

@app.get("/")
def root():
    return {"message": "My name is Ahmad"}

app.include_router(item.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(buying_item.router)