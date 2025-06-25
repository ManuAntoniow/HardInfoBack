from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.userRating import UserRating
from models.product import Producto
from routers.auth import get_current_user
from models.user import User
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/ratings", tags=["ratings"])

class RatingCreate(BaseModel):
    rating: float
    comment: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: float
    comment: Optional[str]
    created_at: str
    user_name: str

    class Config:
        from_attributes = True

class ProductRatingSummary(BaseModel):
    total_rating: float
    rating_count: int
    user_rating: Optional[float] = None

@router.post("/{product_id}", response_model=RatingResponse)
def create_or_update_rating(
    product_id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not 0 <= rating_data.rating <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 0 and 5"
        )
    
    product = db.query(Producto).filter(Producto.id_producto == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    existing_rating = db.query(UserRating).filter(
        UserRating.product_id == product_id,
        UserRating.user_id == current_user.id
    ).first()
    
    if existing_rating:
        existing_rating.rating = rating_data.rating
        existing_rating.comment = rating_data.comment
        db.commit()
        db.refresh(existing_rating)
        rating_to_return = existing_rating
    else:
        new_rating = UserRating(
            product_id=product_id,
            user_id=current_user.id,
            rating=rating_data.rating,
            comment=rating_data.comment
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        rating_to_return = new_rating
    
    update_product_rating(db, product_id)
    
    return RatingResponse(
        id=rating_to_return.id,
        product_id=rating_to_return.product_id,
        user_id=rating_to_return.user_id,
        rating=rating_to_return.rating,
        comment=rating_to_return.comment,
        created_at=rating_to_return.created_at.isoformat(),
        user_name=f"{current_user.nombre} {current_user.apellido}"
    )

@router.get("/{product_id}", response_model=ProductRatingSummary)
def get_product_rating_summary(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Producto).filter(Producto.id_producto == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    user_rating = db.query(UserRating).filter(
        UserRating.product_id == product_id,
        UserRating.user_id == current_user.id
    ).first()
    
    return ProductRatingSummary(
        total_rating=product.total_rating or 0.0,
        rating_count=product.rating_count or 0,
        user_rating=user_rating.rating if user_rating else None
    )

@router.get("/{product_id}/all", response_model=list[RatingResponse])
def get_all_product_ratings(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Producto).filter(Producto.id_producto == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    ratings = db.query(UserRating, User).join(
        User, UserRating.user_id == User.id
    ).filter(UserRating.product_id == product_id).all()
    
    return [
        RatingResponse(
            id=rating.UserRating.id,
            product_id=rating.UserRating.product_id,
            user_id=rating.UserRating.user_id,
            rating=rating.UserRating.rating,
            comment=rating.UserRating.comment,
            created_at=rating.UserRating.created_at.isoformat(),
            user_name=f"{rating.User.nombre} {rating.User.apellido}"
        )
        for rating in ratings
    ]

@router.delete("/{product_id}")
def delete_user_rating(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_rating = db.query(UserRating).filter(
        UserRating.product_id == product_id,
        UserRating.user_id == current_user.id
    ).first()
    
    if not user_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    db.delete(user_rating)
    db.commit()
    
    update_product_rating(db, product_id)
    
    return {"message": "Rating deleted successfully"}

def update_product_rating(db: Session, product_id: int):
    """Función auxiliar para actualizar el promedio de ratings de un producto"""
    result = db.query(
        func.avg(UserRating.rating).label('avg_rating'),
        func.count(UserRating.id).label('count')
    ).filter(UserRating.product_id == product_id).first()
    
    product = db.query(Producto).filter(Producto.id_producto == product_id).first()
    if product:
        product.total_rating = result.avg_rating or 0.0
        product.rating_count = result.count or 0
        db.commit() 