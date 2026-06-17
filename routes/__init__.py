from .dashboard_routes import router as dashboard_router
from .calendario_routes import router as calendario_router
from .cava_routes import router as cava_router
from .general_routes import router as general_router
from .busqueda_routes import router as busqueda_router
from .vino_stats_routes import router as vino_stats_router

__all__ = [
    "dashboard_router",
    "calendario_router",
    "cava_router",
    "general_router",
    "busqueda_router",
    "vino_stats_router"
]