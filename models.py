from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from Project_2.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))