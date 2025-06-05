from fastapi import FastAPI
from routers import auth_router, clients_router, products_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(clients_router, prefix="/clients")
app.include_router(products_router, prefix="/products")

@app.get("/")
def read_root():
    return {"mensagem": "Hello World"}
