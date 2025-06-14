from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Propiedad_ram(Base):
    __tablename__ = "propiedad_ram"

    id_propertie = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"))
    type = Column(String(20))     # DDR4, DDR5, etc.
    size = Column(String(20))     # 8GB, 16GB, 32GB
    speed = Column(String(20))    # 3200MHz, 3600MHz
    latency = Column(String(20))  # CL16, CL18
    format = Column(String(20))   # DIMM, SODIMM
    
    producto = relationship("Producto", back_populates="propiedad_ram", uselist=False)