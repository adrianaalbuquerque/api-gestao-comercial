from fastapi import FastAPI
import uvicorn
from routers import auth_router, clients_router, products_router, orders_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(clients_router, prefix="/clients")
app.include_router(products_router, prefix="/products")
app.include_router(orders_router, prefix="/orders")

@app.get("/")
def read_root():
    return {"mensagem": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)