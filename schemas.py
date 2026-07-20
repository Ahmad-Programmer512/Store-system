from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    name: str
    category: str
    quantity: int
