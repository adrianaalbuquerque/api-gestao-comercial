from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from database.models.client_model import Client
from services.auth_services import get_admin_user
from services import cria_cliente, listar_clientes
from database.engine import SessionLocal
from schemas.schemas import *
from sqlalchemy.orm import Session
from database.models.user_model import User
from services import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def register_client(
    data: Clientes,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    if current_user.user_tipo != "A":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar esta ação."
    )
    try:
        return cria_cliente(data, db, current_user.id)
    except Exception as e:
        #db.rollback()
        return JSONResponse(status_code=400, content={"message": str(e)})
    
@router.get("/", response_model=List[Clientes], status_code=status.HTTP_200_OK)
def get_clientes(
    name: Optional[str] = Query(None, description="Filtro por nome do cliente"),
    email: Optional[str] = Query(None, description="Filtro por email do cliente"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de clientes a retornar"),
    offset: int = Query(0, ge=0, description="Número de clientes a pular"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    clientes = listar_clientes(db=db, user_id=current_user.id, name=name, email=email, limit=limit, offset=offset)
    if not clientes:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado com os filtros aplicados.")
    
    return clientes
