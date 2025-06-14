from sqlalchemy import create_engine
from models.user import User
from models.productFav import FavoriteProduct
from models.product import Producto
from models.gpu import Propiedad_gpu
from models.cpu import Propiedad_cpu
from models.mother import Propiedad_motherboard
from models.ram import Propiedad_ram
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

    productos_data = [
        {
            "id_producto": 1,
            "nombre": "Intel Core i9-13900K",
            "tipo": "CPU",
            "precio": 589.99,
            "descripcion": "16 núcleos/24 hilos, hasta 5.8GHz, socket LGA1700",
            "marca": "Intel"
        },
        {
            "id_producto": 2,
            "nombre": "AMD Ryzen 9 7950X",
            "tipo": "CPU",
            "precio": 699.99,
            "descripcion": "16 núcleos/32 hilos, hasta 5.7GHz, socket AM5",
            "marca": "Amd"
        },
        {
            "id_producto": 7,
            "nombre": "Intel Core i7-13700K",
            "tipo": "CPU",
            "precio": 409.99,
            "descripcion": "16 núcleos/24 hilos, hasta 5.4GHz, socket LGA1700",
            "marca": "Intel"
        },

        # RAMs
        {
            "id_producto": 3,
            "nombre": "Corsair Vengeance RGB 32GB",
            "tipo": "RAM",
            "precio": 129.99,
            "descripcion": "DDR5 5600MHz, CL36, 2x16GB",
            "marca": "Corsair"
        },
        {
            "id_producto": 4,
            "nombre": "G.Skill Trident Z5 64GB",
            "tipo": "RAM",
            "precio": 249.99,
            "descripcion": "DDR5 6000MHz, CL30, 2x32GB",
            "marca": "G.Skill"
        },
        {
            "id_producto": 8,
            "nombre": "Kingston Fury Beast 16GB",
            "tipo": "RAM",
            "precio": 74.99,
            "descripcion": "DDR5 5200MHz, CL40, 2x8GB",
            "marca": "Kingston"
        },

        # GPUs
        {
            "id_producto": 5,
            "nombre": "NVIDIA RTX 4090 Founders Edition",
            "tipo": "GPU",
            "precio": 1599.99,
            "descripcion": "24GB GDDR6X, 16384 CUDA cores",
            "marca": "Nvidia"
        },
        {
            "id_producto": 6,
            "nombre": "AMD Radeon RX 7900 XTX",
            "tipo": "GPU",
            "precio": 999.99,
            "descripcion": "24GB GDDR6, 6144 stream processors",
            "marca": "Amd"
        },
        {
            "id_producto": 9,
            "nombre": "NVIDIA RTX 4070 Ti Super",
            "tipo": "GPU",
            "precio": 799.99,
            "descripcion": "16GB GDDR6X, 8448 CUDA cores",
            "marca": "Nvidia"
        },
        #Motherboards
        {
            "id_producto": 10,
            "nombre": "ASUS ROG Maximus Z790 Hero",
            "tipo": "Motherboard",
            "precio": 599.99,
            "descripcion": "Z790, LGA1700, DDR5, Wi-Fi 6E, PCIe 5.0, ATX",
            "marca": "Asus"
        },
        {
            "id_producto": 11,
            "nombre": "MSI MPG B650 Carbon WiFi",
            "tipo": "Motherboard",
            "precio": 249.99,
            "descripcion": "B650, AM5, DDR5, Wi-Fi 6E, PCIe 4.0, ATX",
            "marca": "MSI"
        },
        {
            "id_producto": 12,
            "nombre": "Gigabyte X670E AORUS Master",
            "tipo": "Motherboard",
            "precio": 449.99,
            "descripcion": "X670E, AM5, DDR5, PCIe 5.0, Wi-Fi 6E, ATX",
            "marca": "Gigabyte"
        }
    ]
    propiedades_cpu_data = [
        {
            "id_producto": 1,
            "threads": 24,
            "cores": 16,
            "frequency": "3.0GHz",
            "boost": "5.8GHz",
            "socket": "LGA1700",
            "cache_l1": 1280,   # en KB (80 KB por core aprox)
            "cache_l2": 20480,  # 20 MB = 20480 KB
            "cache_l3": 36000   # 36 MB = 36000 KB
        },
        {
            "id_producto": 2,
            "threads": 32,
            "cores": 16,
            "frequency": "4.5GHz",
            "boost": "5.7GHz",
            "socket": "AM5",
            "cache_l1": 1024,   # 64 KB por core aprox
            "cache_l2": 16384,  # 16 MB = 16384 KB
            "cache_l3": 64000   # 64 MB = 64000 KB
        },
        {
            "id_producto": 7,
            "threads": 24,
            "cores": 16,
            "frequency": "3.4GHz",
            "boost": "5.4GHz",
            "socket": "LGA1700",
            "cache_l1": 1280,   # igual que el i9-13900K
            "cache_l2": 20480,
            "cache_l3": 30000   # 30 MB = 30000 KB
        }
    ]

    propiedades_ram_data = [
        {
            "id_producto": 3,
            "type": "DDR5",
            "size": "32GB (2x16GB)",
            "speed": "5600MHz",
            "latency": "CL36",
            "format": "DIMM"
        },
        {
            "id_producto": 4,
            "type": "DDR5",
            "size": "64GB (2x32GB)",
            "speed": "6000MHz",
            "latency": "CL30",
            "format": "DIMM"
        },
        {
            "id_producto": 8,
            "type": "DDR5",
            "size": "16GB (2x8GB)",
            "speed": "5200MHz",
            "latency": "CL40",
            "format": "DIMM"
        }
    ]

    propiedades_gpu_data = [
        {
            "id_producto": 5,
            "vram": 24,
            "type_vram": "GDDR6X",
            "connectors_power": "3x 8-pin",
            "tdp": "450W",
            "cores": 16384,
            "tmus": 512,
            "rops": 176,
            "bus_width": 384,
            "length": 304,   # mm
            "width": 137,    # mm
            "height": 61,    # mm
            "suggested_psu": 850
        },
        {
            "id_producto": 6,
            "vram": 24,
            "type_vram": "GDDR6",
            "connectors_power": "2x 8-pin",
            "tdp": "355W",
            "cores": 6144,
            "tmus": 384,
            "rops": 192,
            "bus_width": 384,
            "length": 287,
            "width": 123,
            "height": 51,
            "suggested_psu": 800
        },
        {
            "id_producto": 9,
            "vram": 16,
            "type_vram": "GDDR6X",
            "connectors_power": "1x 16-pin (12VHPWR)",
            "tdp": "285W",
            "cores": 8448,
            "tmus": 264,
            "rops": 96,
            "bus_width": 192,
            "length": 267,
            "width": 112,
            "height": 50,
            "suggested_psu": 700
        }
    ]
    propiedades_motherboard_data = [
        {
            "id_producto": 10,
            "chipset": "Z790",
            "socket": "LGA1700",
            "size_format": "ATX",
            "max_ram": 128,
            "slots_ram": 4,
            "type_ram": "DDR5",
            "slots_pcie_x16": 3,
            "slots_pcie_x1": 2,
            "m2_slots": 5,
            "sata_ports": 6,
            "wifi": True,
            "ethernet_speed": "2.5 Gbps",
            "usb_ports": "4x USB 3.2 Gen 2, 2x USB 2.0",
            "hdmi": True,
            "displayport": True
        },
        {
            "id_producto": 11,
            "chipset": "B650",
            "socket": "AM5",
            "size_format": "ATX",
            "max_ram": 128,
            "slots_ram": 4,
            "type_ram": "DDR5",
            "slots_pcie_x16": 2,
            "slots_pcie_x1": 3,
            "m2_slots": 3,
            "sata_ports": 4,
            "wifi": True,
            "ethernet_speed": "2.5 Gbps",
            "usb_ports": "3x USB 3.2 Gen 2, 4x USB 2.0",
            "hdmi": True,
            "displayport": False
        },
        {
            "id_producto": 12,
            "chipset": "X670E",
            "socket": "AM5",
            "size_format": "ATX",
            "max_ram": 128,
            "slots_ram": 4,
            "type_ram": "DDR5",
            "slots_pcie_x16": 4,
            "slots_pcie_x1": 2,
            "m2_slots": 5,
            "sata_ports": 6,
            "wifi": True,
            "ethernet_speed": "2.5 Gbps",
            "usb_ports": "5x USB 3.2 Gen 2, 2x USB 2.0",
            "hdmi": True,
            "displayport": True
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

    for product_data in productos_data:
        existing_product = db.query(Producto).filter(
            ((Producto.name) == product_data["nombre"])
        ).first()
        if not existing_product:
            db_product = Producto(
                name=product_data["nombre"],
                type=product_data["tipo"],
                price=product_data["precio"],
                brand=product_data["marca"],
                desc=product_data["descripcion"]
            )
            db.add(db_product)

    for cpu_data in propiedades_cpu_data:
        existing_cpu = db.query(Propiedad_cpu).filter(
            Propiedad_cpu.id_producto == cpu_data["id_producto"]
        ).first()
        
        if not existing_cpu:
            db_cpu = Propiedad_cpu(
                id_producto=cpu_data["id_producto"],
                threads=cpu_data["threads"],
                cores=cpu_data["cores"],
                frequency=cpu_data["frequency"],
                boost=cpu_data["boost"],
                socket=cpu_data["socket"],
                cache_l1=cpu_data["cache_l1"],
                cache_l2=cpu_data["cache_l2"],
                cache_l3=cpu_data["cache_l3"]
            )
            db.add(db_cpu)
    
    for ram_data in propiedades_ram_data:
        existing_ram = db.query(Propiedad_ram).filter(
            Propiedad_ram.id_producto == ram_data["id_producto"]
        ).first()
        
        if not existing_ram:
            db_ram = Propiedad_ram(
                id_producto=ram_data["id_producto"],
                type=ram_data["type"],
                size=ram_data["size"],
                speed=ram_data["speed"],
                latency=ram_data["latency"],
                format=ram_data["format"]
            )
            db.add(db_ram)
    

    for gpu_data in propiedades_gpu_data:
        existing_gpu = db.query(Propiedad_gpu).filter(
            Propiedad_gpu.id_producto == gpu_data["id_producto"]
        ).first()
        
        if not existing_gpu:
            db_gpu = Propiedad_gpu(
                id_producto=gpu_data["id_producto"],
                vram=gpu_data["vram"],
                type_vram=gpu_data["type_vram"],
                connectors_power=gpu_data["connectors_power"],
                tdp=gpu_data["tdp"],
                cores=gpu_data["cores"],
                tmus=gpu_data["tmus"],
                rops=gpu_data["rops"],
                bus_width=gpu_data["bus_width"],
                length=gpu_data["length"],
                width=gpu_data["width"],
                height=gpu_data["height"],
                suggested_psu=gpu_data["suggested_psu"]
            )
            db.add(db_gpu)

    for mb_data in propiedades_motherboard_data:
        existing_mb = db.query(Propiedad_motherboard).filter(
            Propiedad_motherboard.id_producto == mb_data["id_producto"]
        ).first()

        if not existing_mb:
            db_mb = Propiedad_motherboard(
                id_producto=mb_data["id_producto"],
                chipset=mb_data["chipset"],
                socket=mb_data["socket"],
                size_format=mb_data["size_format"],
                max_ram=mb_data["max_ram"],
                slots_ram=mb_data["slots_ram"],
                type_ram=mb_data["type_ram"],
                slots_pcie_x16=mb_data["slots_pcie_x16"],
                slots_pcie_x1=mb_data["slots_pcie_x1"],
                m2_slots=mb_data["m2_slots"],
                sata_ports=mb_data["sata_ports"],
                wifi=mb_data["wifi"],
                ethernet_speed=mb_data["ethernet_speed"],
                usb_ports=mb_data["usb_ports"],
                hdmi=mb_data["hdmi"],
                displayport=mb_data["displayport"]
            )
            db.add(db_mb)



    
    db.commit()
    db.close()
    print("Base de datos creada y poblada con datos iniciales")

if __name__ == "__main__":
    create_database()