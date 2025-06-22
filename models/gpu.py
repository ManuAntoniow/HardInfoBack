from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Propiedad_gpu(Base):
    __tablename__ = "propiedad_gpu"

    id_property = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"))
    vram = Column(Integer)          
    type_vram = Column(String(20))            
    connectors_power = Column(String(50))  
    tdp = Column(String(20))
    cores = Column(Integer)
    tmus = Column(Integer)
    rops = Column(Integer)
    bus_width = Column(Integer)
    length = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    suggested_psu = Column(Integer)
    
    producto = relationship("Producto", back_populates="propiedad_gpu", uselist=False)