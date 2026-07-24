from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/item"
)

@router.post("/")
def buy(item_details: schemas.Buying_schema, db: Session = Depends(get_db)):
    query = db.query(models.Item).filter(models.Item.name == item_details.name).first()

    # If query is None
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    # If item quantity more then stoch
    if query.quantity < item_details.quantity and query.quantity > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {query.quantity} items are available in stock.")

    if item_details.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0.")
    
    total_price = query.price * item_details.quantity
    # If given balance is less then required balance
    if item_details.price < total_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient balance. Item costs {query.price * item_details.quantity}, but only {item_details.price} was provided.")
    
    query.quantity -= item_details.quantity

    # If quantity is less then equal 0
    if query.quantity <= 0:
        db.delete(query)

    # If user quantity less then equal


    db.commit()

    return {
        "Item_name": query.name, 
        "Price": query.price,
        "Total_amount": item_details.quantity * query.price,
        "Given_amount": "amount",
        "Remaning_amount": item_details.price - total_price
    }