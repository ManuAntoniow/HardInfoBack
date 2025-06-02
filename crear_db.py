from sqlalchemy import create_engine
from models.user import User
from models.product import FavoriteProduct
from database import Base, get_db
from passlib.context import CryptContext
import os

# Configuración
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_database():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Obtener sesión de base de datos
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Crear usuarios de prueba
    users_data = [
        {
            "nombre": "Juan",
            "apellido": "Pérez",
            "usuario": "juanperez",
            "email": "juan@example.com",
            "password": "password123"
        },
        {
            "nombre": "María",
            "apellido": "Gómez",
            "usuario": "mariag",
            "email": "maria@example.com",
            "password": "securepass"
        }
    ]
    
    for user_data in users_data:

        existing_user = db.query(User).filter(
            (User.email == user_data["email"]) | 
            (User.usuario == user_data["usuario"])
        ).first()
        
        if not existing_user:
            hashed_password = pwd_context.hash(user_data["password"])
            db_user = User(
                nombre=user_data["nombre"],
                apellido=user_data["apellido"],
                usuario=user_data["usuario"],
                email=user_data["email"],
                hashed_password=hashed_password
            )
            db.add(db_user)
    
    db.commit()
    db.close()
    print("Base de datos creada y poblada con datos iniciales")

if __name__ == "__main__":
    create_database()