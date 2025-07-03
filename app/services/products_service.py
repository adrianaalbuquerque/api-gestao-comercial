from decimal import Decimal
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import get_admin_user
from database.models.user_model import User
from database.models.client_model import Client
from database.models import ProductModel
from sqlalchemy.exc import IntegrityError
from schemas.schemas import Product
from typing import List, Optional

def criar_produto(
    db: Session,
    data: Product
    ):
    
    novo_produto = ProductModel(
        descricao = data.descricao,
        valor_venda =  data.valor_venda,
        codigo_barras = data.codigo_barras,
        secao = data.secao,
        estoque = data.estoque,
        data_validade = data.data_validade,
        imagens = None
    )

    produto_existe = db.query(ProductModel).filter_by(codigo_barras = data.codigo_barras).first()
    if produto_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto com código de barras já cadastrado"
        )
    
    try:
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto
    except Exception as e:
        db.rollback()
        if "codigo_barras" in str(e.orig):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Código de barras já cadastrado.")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao tentar inserir novo produto"
        )

def listar_produtos(
    db: Session,
    categoria: Optional[str] = None, #secao
    preco: Optional[Decimal] = None, #valor_venda
    disponibilidade: Optional[bool] = None, #estoque
    limit: int = 10,
    offset: int = 0) -> List[Product]:

    query = db.query(ProductModel)

    if categoria:
        query = query.filter(Product.secao.ilike(f"%{categoria}%"))

    if preco:
        query = query.filter(ProductModel.valor_venda <= preco)

    if disponibilidade is not None:
        if disponibilidade:
            query = query.filter(ProductModel.estoque > 0)
        else:
            query = query.filter(ProductModel.estoque <= 0)

    produtos_orm = query.offset(offset).limit(limit).all()

    produtos = [Product.model_validate(produto) for produto in produtos_orm]
    return produtos

def listar_produto_id(
    db: Session,
    product_id: int
):
    produto = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return Product.model_validate(produto)

def alterar_produto(
        db: Session,
        data: Product,
        product_id: int
):
    produto_existente = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if produto_existente:
       try:
           produto_existente.descricao = data.descricao
           produto_existente.valor_venda = data.valor_venda
           produto_existente.codigo_barras = data.codigo_barras
           produto_existente.secao = data.secao
           produto_existente.estoque = data.estoque
           produto_existente.data_validade = data.data_validade
           produto_existente.imagens = data.imagens

           db.commit()
           db.refresh(produto_existente)
           return produto_existente
       except Exception:
           db.rollback()
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Erro ao tentar atualizar o produto"
           )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não existe"
        )



def deletar_produto(
        db: Session,
        product_id: int
):
    produto_existe = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if produto_existe:
        try:
            db.delete(produto_existe)
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao tenta excluir o produto"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )