from .producto import Producto
from .categoria import Categoria
from .marca import Marca
from .marca_categoria import MarcaCategoria
from .imagenes_producto import ImagenesProducto
from .detalles_producto import (
    DetalleChasis,
    DetalleFuentePoder,
    DetalleMemoriaRAM,
    DetallePlacaBase,
    DetalleProcesador,
    DetalleRefrigeracion,
    DetalleTarjetaGrafica
)

__all__ = [
    'Producto',
    'DetalleChasis',
    'DetalleFuentePoder',
    'DetalleMemoriaRAM',
    'DetallePlacaBase',
    'DetalleProcesador',
    'DetalleRefrigeracion',
    'DetalleTarjetaGrafica',
    'Categoria',
    'Marca',
    'MarcaCategoria',
    'ImagenesProducto'
]