from sqlalchemy import Boolean, Column, Integer, String, Float,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Propiedad_motherboard(Base):
    __tablename__ = "propiedad_motherboard"

    id_propertie = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"))
    chipset = Column(String(50))
    socket = Column(String(20))
    size_format = Column(String(20))  # ATX, Micro-ATX, Mini-ITX, etc.
    max_ram = Column(Integer)          # En GB
    slots_ram = Column(Integer)        
    type_ram = Column(String(10))      # DDR4, DDR5...
    slots_pcie_x16 = Column(Integer)
    slots_pcie_x1 = Column(Integer)
    m2_slots = Column(Integer)
    sata_ports = Column(Integer)
    wifi = Column(Boolean, default=False)
    ethernet_speed = Column(String(20))  # Ej: "1 Gbps", "2.5 Gbps"
    usb_ports = Column(String(100))    # Ej: "2x USB 3.0, 4x USB 2.0"
    hdmi = Column(Boolean, default=False)
    displayport = Column(Boolean, default=False)

    producto = relationship("Producto", back_populates="propiedad_motherboard", uselist=False)
