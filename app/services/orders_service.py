from datetime import date
from fastapi import HTTPException, status
import fastapi
from sqlalchemy import func, select, ScalarSelect, update
from sqlalchemy.orm import Session
from database.models import Client, OrderModel, OrdersProducts, ProductModel
from schemas.schemas import Clientes, ProdutoQuantidade
from typing import List, Dict, Optional

def create_order(database_session: Session, period: date, status: str, id_client: int, products: List[ProdutoQuantidade]):
    new_order: OrderModel

    client = database_session.query(Client).filter(Client.client_id == id_client).first()
    if client == None:
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
    )
    
    products_id = []
    for product in products:
        products_id.append(product.id)
    
    qtd_products = len(products_id)
    existing_products = select(func.count()).select_from(ProductModel).where(ProductModel.id.in_(products_id))
    len_existing_products = database_session.execute(existing_products).scalar_one()
    
    if len_existing_products == qtd_products:
        try:
            new_order = OrderModel (
                period = period,
                status = status,
                id_client = id_client
            )
            database_session.add(new_order)
            database_session.flush()
            id_order = new_order.id

            for product in products:
                estoqueAtual = database_session.execute(select(ProductModel.estoque).where(ProductModel.id == product.id)).scalar_one_or_none()
                
                qtd = product.quantidade
                if estoqueAtual >= qtd:
                        insert_product = OrdersProducts(
                            orders_id = id_order,
                            products_id = product.id,
                            product_qntd = qtd 
                        )

                        diminuindo_estoque = (
                            update(ProductModel)
                            .where(ProductModel.id == product.id)
                            .values(estoque=estoqueAtual - qtd)
                        )

                        database_session.execute(diminuindo_estoque)
                        database_session.add(insert_product)
                        database_session.flush()
                else:
                    database_session.rollback()
                    raise HTTPException(
                        status_code=fastapi.status.HTTP_409_CONFLICT,
                        detail="Estoque insuficiente para o produto")            
            database_session.commit()
            return {"message": "Pedido criado com sucesso", "order_id": id_order}

        except Exception as e:
            database_session.rollback()
            print("Erro real:", e)
            raise

    else:
        database_session.rollback()
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Algum produto da lista não exsite na tabela de produtos"
        )

def list_orders(database_session: Session):
    orders_list = database_session.execute(select(OrderModel)).scalars().all()
    return orders_list

def list_order_byid(database_session: Session, order_id):
    order_list_id = database_session.query(OrderModel).filter(OrderModel.id == order_id).first()
    return order_list_id

def delete_order(database_session: Session, order_id):
    associacoes = database_session.query(OrdersProducts).filter_by(orders_id=order_id).all()
    
    for associacao in associacoes:
        produto = database_session.query(ProductModel).filter_by(id=associacao.products_id).first()
        if produto:
            produto.estoque += associacao.product_qntd
        
        database_session.delete(associacao)

    pedido = database_session.query(OrderModel).filter_by(id=order_id).first()
    if pedido:
        database_session.delete(pedido)

    database_session.commit()


