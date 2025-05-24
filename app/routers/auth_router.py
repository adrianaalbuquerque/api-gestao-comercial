from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.engine import SessionLocal
from database.models.user_model import User
import jwt
import os
from datetime import datetime, timedelta
from services.auth_services import criar_usuario

router = APIRouter()

SENHA_HASH = os.getenv("SENHA_HASH", "senha criptografada")

class LoginData(BaseModel):
    username: str
    senha: str

class RegisterUser(BaseModel):
    id: int
    username: str
    email: str
    tipo: str
    senha: str

db: Session = SessionLocal()

@router.post("/login")
def login(data: LoginData):
    user = db.query(User).filter_by(user_name = data.username).first()
    if not user or user.user_senha != data.senha:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    payload = {
        "user_id": user.id,
        "username": user.user_name,
        "exp": datetime.utcnow() + timedelta(minutes=45)
    }
    token = jwt.encode(payload, SENHA_HASH, algorithm="HS256")
    return {"token": token}


@router.post("/register")
def register(user: RegisterUser):
    db = SessionLocal()
    try:
        novo_usuario = criar_usuario(user, db)
        return {"message": "Usuário criado", "id": novo_usuario.id}
    finally:
        db.close()
    

@router.post("/refresh-token")
def refresh_token():
    pass