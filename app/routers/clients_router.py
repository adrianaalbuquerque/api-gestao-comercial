from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from services.auth_services import get_admin_user
from services import cria_cliente
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

@router.post("/register-client")
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