from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(50))
    price = Column(Numeric(10, 2))
    brand = Column(String(50))
    desc = Column(String(500))

    propiedad_ram = relationship("Propiedad_ram", back_populates="producto")
    propiedad_cpu = relationship("Propiedad_cpu", back_populates="producto")
    propiedad_gpu = relationship("Propiedad_gpu", back_populates="producto")
    propiedad_motherboard = relationship("Propiedad_motherboard", back_populates="producto")