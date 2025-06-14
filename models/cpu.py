from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Propiedad_cpu(Base):
    __tablename__ = "propiedad_cpu"

    id_propertie = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"))
    threads = Column(Integer)
    cores = Column(Integer)
    frequency = Column(String(20))
    boost = Column(String(20))
    socket = Column(String(40))
    cache_l1 = Column(Integer)
    cache_l2 = Column(Integer)
    cache_l3 = Column(Integer)
    
    producto = relationship("Producto", back_populates="propiedad_cpu", uselist=False)