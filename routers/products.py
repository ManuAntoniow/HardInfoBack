from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.product import FavoriteProduct
from database import get_db
from pydantic import BaseModel
from routers.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

class ProductBase(BaseModel):
    product_id: str
    product_name: str

@router.post("/favorites/", status_code=status.HTTP_201_CREATED)
def add_favorite_product(
    product: ProductBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar si el producto ya está en favoritos
    existing_product = db.query(FavoriteProduct).filter(
        FavoriteProduct.product_id == product.product_id,
        FavoriteProduct.owner_id == current_user.id
    ).first()
    
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in favorites"
        )
    
    db_product = FavoriteProduct(
        product_id=product.product_id,
        product_name=product.product_name,
        owner_id=current_user.id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return {"message": "Product added to favorites", "product": db_product}

@router.get("/favorites/")
def get_favorite_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = db.query(FavoriteProduct).filter(
        FavoriteProduct.owner_id == current_user.id
    ).all()
    return products

@router.delete("/favorites/{product_id}")
def remove_favorite_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(FavoriteProduct).filter(
        FavoriteProduct.product_id == product_id,
        FavoriteProduct.owner_id == current_user.id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in favorites"
        )
    
    db.delete(product)
    db.commit()
    
    return {"message": "Product removed from favorites"}