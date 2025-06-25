from sqlalchemy import Column, Integer, String, Numeric, Float
from sqlalchemy.orm import relationship
from database import Base
from models.ram import Propiedad_ram
from models.gpu import Propiedad_gpu
from models.cpu import Propiedad_cpu
from models.mother import Propiedad_motherboard

class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(50))
    price = Column(Numeric(10, 2))
    brand = Column(String(50))
    desc = Column(String(500))
    image = Column(String(500))  # URL de la imagen
    total_rating = Column(Float, default=0.0)  # Promedio de ratings
    rating_count = Column(Integer, default=0)   # Número total de ratings

    propiedad_ram = relationship("Propiedad_ram", back_populates="producto", uselist=False)
    propiedad_cpu = relationship("Propiedad_cpu", back_populates="producto", uselist=False)
    propiedad_gpu = relationship("Propiedad_gpu", back_populates="producto", uselist=False)
    propiedad_motherboard = relationship("Propiedad_motherboard", back_populates="producto", uselist=False)