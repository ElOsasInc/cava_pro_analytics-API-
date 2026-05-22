from .proveedor_routes import router as proveedor_router
from .dashboard_routes import router as dashboard_router
from .calendario_routes import router as calendario_router
from .cava_routes import router as cava_router

__all__ = [
    "proveedor_router",
    "dashboard_router",
    "calendario_router",
    "cava_router"
]