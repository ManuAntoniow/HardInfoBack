from pydantic import BaseModel
from typing import Optional


# ========================
# PROPIEDADES INDIVIDUALES
# ========================

class PropiedadCPUOut(BaseModel):
    id_property: Optional[int] = None
    id_producto: Optional[int] = None
    cores: Optional[int] = None
    threads: Optional[int] = None
    frequency: Optional[str] = None
    boost: Optional[str] = None
    socket: Optional[str] = None
    cache_l1: Optional[int] = None
    cache_l2: Optional[int] = None
    cache_l3: Optional[int] = None

    class Config:
        exclude_none = True
        orm_mode = True



class PropiedadGPUOut(BaseModel):
    id_property: Optional[int] = None
    id_producto: Optional[int] = None
    vram: Optional[int] = None
    type_vram: Optional[str] = None
    connectors_power: Optional[str] = None
    tdp: Optional[str] = None
    cores: Optional[int] = None
    tmus: Optional[int] = None
    rops: Optional[int] = None
    bus_width: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    suggested_psu: Optional[int] = None

    class Config:
        exclude_none = True
        orm_mode = True



class PropiedadRAMOut(BaseModel):
    id_property: Optional[int] = None
    id_producto: Optional[int] = None
    type: Optional[str] = None
    size: Optional[str] = None
    speed: Optional[str] = None
    latency: Optional[str] = None
    format: Optional[str] = None

    class Config:
        exclude_none = True
        orm_mode = True


class PropiedadMotherboardOut(BaseModel):
    id_property: Optional[int] = None
    id_producto: Optional[int] = None
    chipset: Optional[str] = None
    socket: Optional[str] = None
    size_format: Optional[str] = None
    max_ram: Optional[int] = None
    slots_ram: Optional[int] = None
    type_ram: Optional[str] = None
    slots_pcie_x16: Optional[int] = None
    slots_pcie_x1: Optional[int] = None
    m2_slots: Optional[int] = None
    sata_ports: Optional[int] = None
    wifi: Optional[bool] = None
    ethernet_speed: Optional[str] = None
    usb_ports: Optional[str] = None
    hdmi: Optional[bool] = None
    displayport: Optional[bool] = None

    class Config:
        exclude_none = True
        orm_mode = True


# ========================
# PRODUCTO GENERAL
# ========================

class ProductoOut(BaseModel):
    id_producto: int
    name: str
    type: str
    price: float
    brand: str
    desc: Optional[str]
    image: Optional[str]

    propiedad_cpu: Optional[PropiedadCPUOut]
    propiedad_gpu: Optional[PropiedadGPUOut]
    propiedad_ram: Optional[PropiedadRAMOut]
    propiedad_motherboard: Optional[PropiedadMotherboardOut]

    class Config:
        orm_mode = True
