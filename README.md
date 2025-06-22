# HardInfoBack
Back de HardInfo con FastAPI y SQlite

Por el momento solo registro y login.

La bd, como es sqlite, es un archivo local.

Para levantarlo tiren "python -m uvicorn main:app --reload"
Acuerdense de instalar todas las librerias del requirements.txt

http://localhost:8000/auth/register
body:
{
    "nombre": "Ian",
    "apellido": "Campo",
    "usuario": "Oniloco",
    "email": "Oniloco@example.com",
    "password": "Bananon"
}

http://localhost:8000/auth/token
form con
username=Oniloco
password=Bananon

Te genera un token, dura 30 minutos, se puede cambiar en auth.py

# HardInfo Backend API

API REST para gestión de productos de hardware informático.

## Endpoints de Productos

### Búsqueda General

#### `GET /products/search`
Búsqueda general de productos con filtros básicos.

**Parámetros:**
- `type` (opcional): Tipo de producto (CPU, GPU, RAM, Motherboard)
- `brand` (opcional): Marca del producto
- `min_price` (opcional): Precio mínimo
- `max_price` (opcional): Precio máximo
- `min_cores` (opcional): Número mínimo de núcleos (para CPUs)
- `min_threads` (opcional): Número mínimo de hilos (para CPUs)
- `min_vram` (opcional): VRAM mínimo en GB (para GPUs)

**Ejemplo:**
```
GET /products/search?type=CPU&brand=AMD&min_price=100&max_price=500&min_cores=6
```

### Búsqueda Específica por Tipo

#### `GET /products/cpus`
Buscar CPUs por características específicas.

**Parámetros:**
- `brand` (opcional): Marca del CPU
- `min_cores` (opcional): Número mínimo de núcleos
- `max_cores` (opcional): Número máximo de núcleos
- `min_threads` (opcional): Número mínimo de hilos
- `max_threads` (opcional): Número máximo de hilos
- `socket` (opcional): Tipo de socket (ej: AM4, LGA1200)
- `min_frequency` (opcional): Frecuencia base mínima en GHz
- `max_frequency` (opcional): Frecuencia base máxima en GHz
- `min_price` (opcional): Precio mínimo
- `max_price` (opcional): Precio máximo

**Ejemplo:**
```
GET /products/cpus?brand=Intel&min_cores=8&socket=LGA1200&min_price=200
```

#### `GET /products/gpus`
Buscar GPUs por características específicas.

**Parámetros:**
- `brand` (opcional): Marca de la GPU
- `min_vram` (opcional): VRAM mínimo en GB
- `max_vram` (opcional): VRAM máximo en GB
- `type_vram` (opcional): Tipo de VRAM (ej: GDDR6, GDDR6X)
- `min_cores` (opcional): Número mínimo de cores
- `max_cores` (opcional): Número máximo de cores
- `min_bus_width` (opcional): Ancho de bus mínimo en bits
- `max_bus_width` (opcional): Ancho de bus máximo en bits
- `min_length` (opcional): Longitud mínima en mm
- `max_length` (opcional): Longitud máxima en mm
- `min_price` (opcional): Precio mínimo
- `max_price` (opcional): Precio máximo

**Ejemplo:**
```
GET /products/gpus?brand=NVIDIA&min_vram=8&type_vram=GDDR6&min_price=300
```

#### `GET /products/rams`
Buscar RAM por características específicas.

**Parámetros:**
- `brand` (opcional): Marca de la RAM
- `type` (opcional): Tipo de RAM (ej: DDR4, DDR5)
- `size` (opcional): Tamaño (ej: 8GB, 16GB, 32GB)
- `speed` (opcional): Velocidad (ej: 3200MHz, 3600MHz)
- `latency` (opcional): Latencia (ej: CL16, CL18)
- `format` (opcional): Formato (DIMM, SODIMM)
- `min_price` (opcional): Precio mínimo
- `max_price` (opcional): Precio máximo

**Ejemplo:**
```
GET /products/rams?type=DDR4&size=16GB&speed=3200MHz&min_price=50
```

#### `GET /products/motherboards`
Buscar motherboards por características específicas.

**Parámetros:**
- `brand` (opcional): Marca de la motherboard
- `chipset` (opcional): Chipset (ej: B550, X570, Z690)
- `socket` (opcional): Socket (ej: AM4, LGA1200, LGA1700)
- `size_format` (opcional): Formato (ATX, Micro-ATX, Mini-ITX)
- `type_ram` (opcional): Tipo de RAM soportada (DDR4, DDR5)
- `min_ram_slots` (opcional): Número mínimo de slots RAM
- `max_ram_slots` (opcional): Número máximo de slots RAM
- `min_max_ram` (opcional): RAM máxima mínima en GB
- `max_max_ram` (opcional): RAM máxima máxima en GB
- `min_m2_slots` (opcional): Número mínimo de slots M.2
- `max_m2_slots` (opcional): Número máximo de slots M.2
- `wifi` (opcional): Con WiFi integrado (true/false)
- `min_price` (opcional): Precio mínimo
- `max_price` (opcional): Precio máximo

**Ejemplo:**
```
GET /products/motherboards?chipset=B550&socket=AM4&wifi=true&min_price=100
```

### Búsqueda Avanzada

#### `GET /products/advanced-search`
Búsqueda avanzada que combina filtros de diferentes tipos de productos.

**Parámetros:**
- `type` (opcional): Tipo de producto
- `brand` (opcional): Marca
- `min_price` (opcional): Precio mínimo
- `max_price` (opcional): Precio máximo
- `min_cpu_cores` (opcional): Número mínimo de núcleos de CPU
- `max_cpu_cores` (opcional): Número máximo de núcleos de CPU
- `cpu_socket` (opcional): Socket de CPU
- `min_gpu_vram` (opcional): VRAM mínimo de GPU
- `max_gpu_vram` (opcional): VRAM máximo de GPU
- `gpu_type_vram` (opcional): Tipo de VRAM de GPU
- `ram_type` (opcional): Tipo de RAM
- `ram_size` (opcional): Tamaño de RAM
- `mb_chipset` (opcional): Chipset de motherboard
- `mb_socket` (opcional): Socket de motherboard
- `mb_format` (opcional): Formato de motherboard

**Ejemplo:**
```
GET /products/advanced-search?type=CPU&min_cpu_cores=6&cpu_socket=AM4&min_price=200
```

### Listado General

#### `GET /products/all-cpus`
Obtener todos los CPUs sin filtros.

#### `GET /products/all-gpus`
Obtener todas las GPUs sin filtros.

#### `GET /products/all-rams`
Obtener todas las RAMs sin filtros.

#### `GET /products/all-motherboards`
Obtener todas las motherboards sin filtros.

#### `GET /products/all-products`
Obtener todos los productos sin filtros.

### Producto Específico

#### `GET /products/{product_id}`
Obtener un producto específico por su ID.

**Ejemplo:**
```
GET /products/1
```

### Búsqueda por Marca

#### `GET /products/brand/{brand_name}`
Obtener todos los productos de una marca específica.

**Ejemplo:**
```
GET /products/brand/AMD
```

### Favoritos (Requiere Autenticación)

#### `POST /products/favorites/`
Agregar un producto a favoritos.

**Body:**
```json
{
    "product_id": "1",
    "product_name": "AMD Ryzen 7 5800X"
}
```

#### `GET /products/favorites/`
Obtener productos favoritos del usuario.

#### `DELETE /products/favorites/{product_id}`
Eliminar un producto de favoritos.

## Autenticación

Los endpoints de favoritos requieren autenticación mediante JWT token.

**Header requerido:**
```
Authorization: Bearer <token>
```

## Respuestas

Todos los endpoints devuelven productos en el siguiente formato:

```json
{
    "id_producto": 1,
    "name": "AMD Ryzen 7 5800X",
    "type": "CPU",
    "price": 299.99,
    "brand": "AMD",
    "desc": "Procesador de 8 núcleos y 16 hilos",
    "propiedad_cpu": {
        "id_property": 1,
        "id_producto": 1,
        "cores": 8,
        "threads": 16,
        "frequency": "3.8",
        "boost": "4.7",
        "socket": "AM4"
    },
    "propiedad_gpu": null,
    "propiedad_ram": null,
    "propiedad_motherboard": null
}
```

## Códigos de Estado

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Datos de entrada inválidos
- `401 Unauthorized`: No autorizado
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error interno del servidor
