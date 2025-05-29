from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.models.client_model import Client
from database.models.user_model import User
from sqlalchemy.exc import IntegrityError
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
