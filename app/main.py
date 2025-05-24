from typing import Union
from fastapi import FastAPI
from routers import auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def read_root():
    return {"mensagem": "Hello World"}
