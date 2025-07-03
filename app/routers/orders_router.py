from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from services import create_order, list_orders, list_order_byid, delete_order
from database.models.order_model import OrderModel
from database.engine import SessionLocal
from schemas.schemas import *
from sqlalchemy.orm import Session
from database.models import order_model, orders_products

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def orders_create(
    order: Orders,
    db: Session = Depends(get_db),
):
    return create_order(
        database_session=db,
        period=order.period,
        status=order.status,
        id_client=order.client_id,
        products=order.product_quantity
    )

@router.get("/")
def list_all_orders(
    db: Session = Depends(get_db)
):
    return list_orders(database_session=db)

@router.get("/{order_id}")
def list_by_id(
    order_id = int,
    db: Session = Depends(get_db)
):
    return list_order_byid(database_session=db, order_id=order_id)

@router.delete("/{order_id}")
def delete_order_by_id(
    order_id = int,
    db: Session = Depends(get_db)
):
    return delete_order(database_session=db, order_id=order_id)