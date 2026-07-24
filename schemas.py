from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Item(BaseModel):
    name: str
    price: int
    category: str
    quantity: int

class Item_Response(BaseModel):
    id: int
    name: str
    price: int
    category: str
    quantity: int
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Buying_schema(BaseModel):
    name: str
    price: int
    quantity: int