from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from services import *
from database.engine import SessionLocal
from schemas.schemas import Product
from sqlalchemy.orm import Session
from services import criar_produto, listar_produtos, listar_produto_id, alterar_produto
from database.models.user_model import User


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_product(
    data: Product,
    user_id: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    return criar_produto(db=db, current_user=user_id, data=data)

@router.get("/", response_model=List[Product])
def get_products(
    categoria: Optional[str] = Query(None),
    preco: Optional[Decimal] = Query(None),
    disponibilidade: Optional[bool] = Query(None),
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return listar_produtos(db, categoria, preco, disponibilidade, limit, offset)

@router.get("/{id}", response_model=Product)
def get_products_id(
    id: int,
    db: Session = Depends(get_db)
):
    produto = listar_produto_id(db=db, product_id=id)
    return produto

@router.put("/{id}")
def update_product(
    id: int,
    data: Product,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    return alterar_produto(db=db, data=data, user_id=current_user, product_id=id)

@router.delete("/")
def delete_product(

):
    return