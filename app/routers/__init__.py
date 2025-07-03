from .auth_router import router as auth_router
from .clients_router import router as clients_router
from .products_router import router as products_router
from .orders_router import router as orders_router

__all__ = ["auth_router", "clients_router", "products_router", "orders_router"]
