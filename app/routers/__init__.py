from .auth_router import router as auth_router
from .clients_router import router as clients_router
from .products_router import router as products_router

__all__ = ["auth_router", "clients_router", "products_router"]
