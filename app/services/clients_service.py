from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.models.client_model import Client
from schemas.schemas import Clientes
from typing import List, Optional

def cria_cliente(data: Clientes, db: Session, user_id: int) -> Client:
    existente = db.query(Client).filter_by(client_cpf=data.cpf).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente já cadastrado"
        )

    novo_cliente = Client(
        client_cpf=data.cpf,
        client_email=data.email,
        client_name=data.name,
        usuario_id=user_id
    )
    try:
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        return novo_cliente
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar cliente"
        )

def listar_clientes(db: Session, user_id: int, name: Optional[str] = None, email: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[Clientes]:
    query = db.query(Client).filter(Client.usuario_id == user_id)

    if name:
        query = query.filter(Client.client_name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.client_email.ilike(f"%{email}%"))

    clientes_orm = query.offset(offset).limit(limit).all()

    clientes = []
    for c in clientes_orm:
        cliente = Clientes(
            cpf=c.client_cpf,
            email=c.client_email,
            name=c.client_name
    )        
        clientes.append(cliente)

    return clientes

def buscar_cliente_por_id(db: Session, user_id: int, cliente_id: int) -> Optional[Clientes]:
    cliente_orm = (
        db.query(Client)
        .filter(Client.usuario_id == user_id, Client.client_id == cliente_id)
        .first()
    )

    if not cliente_orm:
        return None

    return Clientes(
        cpf=cliente_orm.client_cpf,
        email=cliente_orm.client_email,
        name=cliente_orm.client_name,
    )

def atualiza_cliente(db: Session, user_id: int, data: Clientes, id: int) -> Client:
    cliente = db.query(Client).filter_by(client_id = id).first()
    if cliente:
        try:
            cliente.client_cpf = data.client_cpf
            cliente.client_email = data.client_email
            cliente.client_name = data.client_name
            cliente.usuario_id = user_id

            db.commit()
            db.refresh(cliente)
            return cliente

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar o cliente"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="O cliente não existe"
        )

def deletar_cliente(db: Session, id: int):
    cliente = db.query(Client).filter_by(client_id = id).first()
    if cliente:
        try:
            db.delete(cliente)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao tentar deletar cliente"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não existe"
        )