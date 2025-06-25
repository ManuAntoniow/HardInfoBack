from sqlalchemy import Column, Integer, Float, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class UserRating(Base):
    __tablename__ = "user_ratings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=False)  # Rating de 0 a 5
    comment = Column(Text, nullable=True)   # Comentario opcional
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 