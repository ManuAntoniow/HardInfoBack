from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from models.gpu import Propiedad_gpu
from models.product import Producto
from models.cpu import Propiedad_cpu
from models.ram import Propiedad_ram
from models.mother import Propiedad_motherboard
from sqlalchemy.orm import joinedload
from models.user import User
from models.productFav import FavoriteProduct
from database import get_db
from pydantic import BaseModel
from routers.auth import get_current_user
from schemas import ProductoOut

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
    
@router.get("/search", response_model=list[ProductoOut])
def buscar_productos(
    type: Optional[str] = Query(None, description="Tipo de producto, ej: CPU, GPU, RAM, Motherboard"),
    brand: Optional[str] = Query(None, description="Marca del producto"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_cores: Optional[int] = Query(None, ge=0),
    min_threads: Optional[int] = Query(None, ge=0),
    min_vram: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Producto)
    
    # Carga eager de las relaciones según el tipo
    if type:
        type_lower = type.lower()
        if type_lower == "gpu":
            query = query.options(joinedload(Producto.propiedad_gpu))
        elif type_lower == "cpu":
            query = query.options(joinedload(Producto.propiedad_cpu))
        elif type_lower == "ram":
            query = query.options(joinedload(Producto.propiedad_ram))
        elif type_lower == "motherboard":
            query = query.options(joinedload(Producto.propiedad_motherboard))
    else:
        # Si no hay tipo, cargar todas las relaciones (puede ser costoso)
        query = query.options(
            joinedload(Producto.propiedad_cpu),
            joinedload(Producto.propiedad_gpu),
            joinedload(Producto.propiedad_ram),
            joinedload(Producto.propiedad_motherboard),
        )

    # Filtros generales
    if type:
        query = query.filter(Producto.type.ilike(f"%{type}%"))

    if brand:
        query = query.filter(Producto.brand.ilike(f"%{brand}%"))

    if min_price is not None:
        query = query.filter(Producto.price >= min_price)

    if max_price is not None:
        query = query.filter(Producto.price <= max_price)

    # Filtros específicos según el tipo
    if type and type_lower == "gpu":
        query = query.join(Producto.propiedad_gpu)
        if min_vram is not None:
            query = query.filter(Propiedad_gpu.vram >= min_vram)

    elif type and type_lower == "cpu":
        query = query.join(Producto.propiedad_cpu)
        if min_cores is not None:
            query = query.filter(Propiedad_cpu.cores >= min_cores)
        if min_threads is not None:
            query = query.filter(Propiedad_cpu.threads >= min_threads)

    elif type and type_lower == "ram":
        query = query.join(Producto.propiedad_ram)

    productos = query.all()
    return productos

# ========================
# ENDPOINTS ESPECÍFICOS POR TIPO
# ========================

@router.get("/cpus", response_model=List[ProductoOut])
def buscar_cpus(
    brand: Optional[str] = Query(None, description="Marca del CPU"),
    min_cores: Optional[int] = Query(None, ge=0, description="Número mínimo de núcleos"),
    max_cores: Optional[int] = Query(None, ge=0, description="Número máximo de núcleos"),
    min_threads: Optional[int] = Query(None, ge=0, description="Número mínimo de hilos"),
    max_threads: Optional[int] = Query(None, ge=0, description="Número máximo de hilos"),
    socket: Optional[str] = Query(None, description="Tipo de socket (ej: AM4, LGA1200)"),
    min_frequency: Optional[float] = Query(None, ge=0, description="Frecuencia base mínima en GHz"),
    max_frequency: Optional[float] = Query(None, ge=0, description="Frecuencia base máxima en GHz"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """Buscar CPUs por características específicas"""
    # Usar LEFT JOIN para incluir todas las CPUs, incluso sin propiedades
    query = db.query(Producto).outerjoin(Producto.propiedad_cpu).options(
        joinedload(Producto.propiedad_cpu)
    ).filter(Producto.type.ilike("%cpu%"))

    if brand:
        query = query.filter(Producto.brand.ilike(f"%{brand}%"))
    
    if min_cores is not None:
        query = query.filter(Propiedad_cpu.cores >= min_cores)
    
    if max_cores is not None:
        query = query.filter(Propiedad_cpu.cores <= max_cores)
    
    if min_threads is not None:
        query = query.filter(Propiedad_cpu.threads >= min_threads)
    
    if max_threads is not None:
        query = query.filter(Propiedad_cpu.threads <= max_threads)
    
    if socket:
        query = query.filter(Propiedad_cpu.socket.ilike(f"%{socket}%"))
    
    if min_frequency is not None:
        query = query.filter(Propiedad_cpu.frequency >= str(min_frequency))
    
    if max_frequency is not None:
        query = query.filter(Propiedad_cpu.frequency <= str(max_frequency))
    
    if min_price is not None:
        query = query.filter(Producto.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Producto.price <= max_price)

    return query.all()

@router.get("/gpus", response_model=List[ProductoOut])
def buscar_gpus(
    brand: Optional[str] = Query(None, description="Marca de la GPU"),
    min_vram: Optional[int] = Query(None, ge=0, description="VRAM mínimo en GB"),
    max_vram: Optional[int] = Query(None, ge=0, description="VRAM máximo en GB"),
    type_vram: Optional[str] = Query(None, description="Tipo de VRAM (ej: GDDR6, GDDR6X)"),
    min_cores: Optional[int] = Query(None, ge=0, description="Número mínimo de cores"),
    max_cores: Optional[int] = Query(None, ge=0, description="Número máximo de cores"),
    min_bus_width: Optional[int] = Query(None, ge=0, description="Ancho de bus mínimo en bits"),
    max_bus_width: Optional[int] = Query(None, ge=0, description="Ancho de bus máximo en bits"),
    min_length: Optional[int] = Query(None, ge=0, description="Longitud mínima en mm"),
    max_length: Optional[int] = Query(None, ge=0, description="Longitud máxima en mm"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """Buscar GPUs por características específicas"""
    # Usar LEFT JOIN para incluir todas las GPUs, incluso sin propiedades
    query = db.query(Producto).outerjoin(Producto.propiedad_gpu).options(
        joinedload(Producto.propiedad_gpu)
    ).filter(Producto.type.ilike("%gpu%"))

    if brand:
        query = query.filter(Producto.brand.ilike(f"%{brand}%"))
    
    if min_vram is not None:
        query = query.filter(Propiedad_gpu.vram >= min_vram)
    
    if max_vram is not None:
        query = query.filter(Propiedad_gpu.vram <= max_vram)
    
    if type_vram:
        query = query.filter(Propiedad_gpu.type_vram.ilike(f"%{type_vram}%"))
    
    if min_cores is not None:
        query = query.filter(Propiedad_gpu.cores >= min_cores)
    
    if max_cores is not None:
        query = query.filter(Propiedad_gpu.cores <= max_cores)
    
    if min_bus_width is not None:
        query = query.filter(Propiedad_gpu.bus_width >= min_bus_width)
    
    if max_bus_width is not None:
        query = query.filter(Propiedad_gpu.bus_width <= max_bus_width)
    
    if min_length is not None:
        query = query.filter(Propiedad_gpu.length >= min_length)
    
    if max_length is not None:
        query = query.filter(Propiedad_gpu.length <= max_length)
    
    if min_price is not None:
        query = query.filter(Producto.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Producto.price <= max_price)

    return query.all()

@router.get("/rams", response_model=List[ProductoOut])
def buscar_rams(
    brand: Optional[str] = Query(None, description="Marca de la RAM"),
    type: Optional[str] = Query(None, description="Tipo de RAM (ej: DDR4, DDR5)"),
    size: Optional[str] = Query(None, description="Tamaño (ej: 8GB, 16GB, 32GB)"),
    speed: Optional[str] = Query(None, description="Velocidad (ej: 3200MHz, 3600MHz)"),
    latency: Optional[str] = Query(None, description="Latencia (ej: CL16, CL18)"),
    format: Optional[str] = Query(None, description="Formato (DIMM, SODIMM)"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """Buscar RAM por características específicas"""
    # Usar LEFT JOIN para incluir todas las RAMs, incluso sin propiedades
    query = db.query(Producto).outerjoin(Producto.propiedad_ram).options(
        joinedload(Producto.propiedad_ram)
    ).filter(Producto.type.ilike("%ram%"))

    if brand:
        query = query.filter(Producto.brand.ilike(f"%{brand}%"))
    
    if type:
        query = query.filter(Propiedad_ram.type.ilike(f"%{type}%"))
    
    if size:
        query = query.filter(Propiedad_ram.size.ilike(f"%{size}%"))
    
    if speed:
        query = query.filter(Propiedad_ram.speed.ilike(f"%{speed}%"))
    
    if latency:
        query = query.filter(Propiedad_ram.latency.ilike(f"%{latency}%"))
    
    if format:
        query = query.filter(Propiedad_ram.format.ilike(f"%{format}%"))
    
    if min_price is not None:
        query = query.filter(Producto.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Producto.price <= max_price)

    return query.all()

@router.get("/motherboards", response_model=List[ProductoOut])
def buscar_motherboards(
    brand: Optional[str] = Query(None, description="Marca de la motherboard"),
    chipset: Optional[str] = Query(None, description="Chipset (ej: B550, X570, Z690)"),
    socket: Optional[str] = Query(None, description="Socket (ej: AM4, LGA1200, LGA1700)"),
    size_format: Optional[str] = Query(None, description="Formato (ATX, Micro-ATX, Mini-ITX)"),
    type_ram: Optional[str] = Query(None, description="Tipo de RAM soportada (DDR4, DDR5)"),
    min_ram_slots: Optional[int] = Query(None, ge=0, description="Número mínimo de slots RAM"),
    max_ram_slots: Optional[int] = Query(None, ge=0, description="Número máximo de slots RAM"),
    min_max_ram: Optional[int] = Query(None, ge=0, description="RAM máxima mínima en GB"),
    max_max_ram: Optional[int] = Query(None, ge=0, description="RAM máxima máxima en GB"),
    min_m2_slots: Optional[int] = Query(None, ge=0, description="Número mínimo de slots M.2"),
    max_m2_slots: Optional[int] = Query(None, ge=0, description="Número máximo de slots M.2"),
    wifi: Optional[bool] = Query(None, description="Con WiFi integrado"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """Buscar motherboards por características específicas"""
    # Usar LEFT JOIN para incluir todas las motherboards, incluso sin propiedades
    query = db.query(Producto).outerjoin(Producto.propiedad_motherboard).options(
        joinedload(Producto.propiedad_motherboard)
    ).filter(Producto.type.ilike("%motherboard%"))

    if brand:
        query = query.filter(Producto.brand.ilike(f"%{brand}%"))
    
    if chipset:
        query = query.filter(Propiedad_motherboard.chipset.ilike(f"%{chipset}%"))
    
    if socket:
        query = query.filter(Propiedad_motherboard.socket.ilike(f"%{socket}%"))
    
    if size_format:
        query = query.filter(Propiedad_motherboard.size_format.ilike(f"%{size_format}%"))
    
    if type_ram:
        query = query.filter(Propiedad_motherboard.type_ram.ilike(f"%{type_ram}%"))
    
    if min_ram_slots is not None:
        query = query.filter(Propiedad_motherboard.slots_ram >= min_ram_slots)
    
    if max_ram_slots is not None:
        query = query.filter(Propiedad_motherboard.slots_ram <= max_ram_slots)
    
    if min_max_ram is not None:
        query = query.filter(Propiedad_motherboard.max_ram >= min_max_ram)
    
    if max_max_ram is not None:
        query = query.filter(Propiedad_motherboard.max_ram <= max_max_ram)
    
    if min_m2_slots is not None:
        query = query.filter(Propiedad_motherboard.m2_slots >= min_m2_slots)
    
    if max_m2_slots is not None:
        query = query.filter(Propiedad_motherboard.m2_slots <= max_m2_slots)
    
    if wifi is not None:
        query = query.filter(Propiedad_motherboard.wifi == wifi)
    
    if min_price is not None:
        query = query.filter(Producto.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Producto.price <= max_price)

    return query.all()

# ========================
# ENDPOINTS DE BÚSQUEDA AVANZADA
# ========================

@router.get("/advanced-search", response_model=List[ProductoOut])
def busqueda_avanzada(
    # Filtros generales
    type: Optional[str] = Query(None, description="Tipo de producto"),
    brand: Optional[str] = Query(None, description="Marca"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    
    # Filtros específicos de CPU
    min_cpu_cores: Optional[int] = Query(None, ge=0),
    max_cpu_cores: Optional[int] = Query(None, ge=0),
    cpu_socket: Optional[str] = Query(None),
    
    # Filtros específicos de GPU
    min_gpu_vram: Optional[int] = Query(None, ge=0),
    max_gpu_vram: Optional[int] = Query(None, ge=0),
    gpu_type_vram: Optional[str] = Query(None),
    
    # Filtros específicos de RAM
    ram_type: Optional[str] = Query(None),
    ram_size: Optional[str] = Query(None),
    
    # Filtros específicos de Motherboard
    mb_chipset: Optional[str] = Query(None),
    mb_socket: Optional[str] = Query(None),
    mb_format: Optional[str] = Query(None),
    
    db: Session = Depends(get_db)
):
    """Búsqueda avanzada que combina filtros de diferentes tipos de productos"""
    query = db.query(Producto)
    
    # Cargar todas las relaciones
    query = query.options(
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_ram),
        joinedload(Producto.propiedad_motherboard),
    )

    # Filtros generales
    if type:
        query = query.filter(Producto.type.ilike(f"%{type}%"))
    
    if brand:
        query = query.filter(Producto.brand.ilike(f"%{brand}%"))
    
    if min_price is not None:
        query = query.filter(Producto.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Producto.price <= max_price)

    # Filtros específicos por tipo
    if type and type.lower() == "cpu":
        query = query.join(Producto.propiedad_cpu)
        if min_cpu_cores is not None:
            query = query.filter(Propiedad_cpu.cores >= min_cpu_cores)
        if max_cpu_cores is not None:
            query = query.filter(Propiedad_cpu.cores <= max_cpu_cores)
        if cpu_socket:
            query = query.filter(Propiedad_cpu.socket.ilike(f"%{cpu_socket}%"))
    
    elif type and type.lower() == "gpu":
        query = query.join(Producto.propiedad_gpu)
        if min_gpu_vram is not None:
            query = query.filter(Propiedad_gpu.vram >= min_gpu_vram)
        if max_gpu_vram is not None:
            query = query.filter(Propiedad_gpu.vram <= max_gpu_vram)
        if gpu_type_vram:
            query = query.filter(Propiedad_gpu.type_vram.ilike(f"%{gpu_type_vram}%"))
    
    elif type and type.lower() == "ram":
        query = query.join(Producto.propiedad_ram)
        if ram_type:
            query = query.filter(Propiedad_ram.type.ilike(f"%{ram_type}%"))
        if ram_size:
            query = query.filter(Propiedad_ram.size.ilike(f"%{ram_size}%"))
    
    elif type and type.lower() == "motherboard":
        query = query.join(Producto.propiedad_motherboard)
        if mb_chipset:
            query = query.filter(Propiedad_motherboard.chipset.ilike(f"%{mb_chipset}%"))
        if mb_socket:
            query = query.filter(Propiedad_motherboard.socket.ilike(f"%{mb_socket}%"))
        if mb_format:
            query = query.filter(Propiedad_motherboard.size_format.ilike(f"%{mb_format}%"))

    return query.all()

# ========================
# ENDPOINTS DE LISTADO GENERAL
# ========================

@router.get("/all-gpus", response_model=List[ProductoOut])
def get_all_gpus(db: Session = Depends(get_db)):
    """Obtener todas las GPUs sin filtros"""
    productos = db.query(Producto).outerjoin(Producto.propiedad_gpu).options(
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_ram),
        joinedload(Producto.propiedad_motherboard),
    ).filter(Producto.type.ilike("gpu")).all()

    return productos

@router.get("/all-cpus", response_model=List[ProductoOut])
def get_all_cpus(db: Session = Depends(get_db)):
    """Obtener todos los CPUs sin filtros"""
    productos = db.query(Producto).outerjoin(Producto.propiedad_cpu).options(
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_ram),
        joinedload(Producto.propiedad_motherboard),
    ).filter(Producto.type.ilike("cpu")).all()

    return productos

@router.get("/all-rams", response_model=List[ProductoOut])
def get_all_rams(db: Session = Depends(get_db)):
    """Obtener todas las RAMs sin filtros"""
    productos = db.query(Producto).outerjoin(Producto.propiedad_ram).options(
        joinedload(Producto.propiedad_ram),
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_motherboard),
    ).filter(Producto.type.ilike("ram")).all()

    return productos

@router.get("/all-motherboards", response_model=List[ProductoOut])
def get_all_motherboards(db: Session = Depends(get_db)):
    """Obtener todas las motherboards sin filtros"""
    productos = db.query(Producto).outerjoin(Producto.propiedad_motherboard).options(
        joinedload(Producto.propiedad_motherboard),
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_ram),
    ).filter(Producto.type.ilike("motherboard")).all()

    return productos

@router.get("/all-products", response_model=List[ProductoOut])
def get_all_products(db: Session = Depends(get_db)):
    """Obtener todos los productos sin filtros"""
    productos = db.query(Producto).options(
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_ram),
        joinedload(Producto.propiedad_motherboard),
    ).all()

    return productos

# ========================
# ENDPOINTS DE PRODUCTO ESPECÍFICO
# ========================

@router.get("/{product_id}", response_model=ProductoOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Obtener un producto específico por su ID"""
    producto = db.query(Producto).options(
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_ram),
        joinedload(Producto.propiedad_motherboard),
    ).filter(Producto.id_producto == product_id).first()
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    return producto

# ========================
# ENDPOINTS DE BÚSQUEDA POR MARCA
# ========================

@router.get("/brand/{brand_name}", response_model=List[ProductoOut])
def get_products_by_brand(brand_name: str, db: Session = Depends(get_db)):
    """Obtener todos los productos de una marca específica"""
    productos = db.query(Producto).options(
        joinedload(Producto.propiedad_cpu),
        joinedload(Producto.propiedad_gpu),
        joinedload(Producto.propiedad_ram),
        joinedload(Producto.propiedad_motherboard),
    ).filter(Producto.brand.ilike(f"%{brand_name}%")).all()
    
    return productos



