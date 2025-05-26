from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from database.engine import SessionLocal
from database.models.user_model import User
from jose import jwt
from datetime import datetime, timedelta
from services.auth_services import *
from schemas.schemas import *

router = APIRouter()

@router.post("/login")
def login(data: LoginData):
    db = SessionLocal()
    try:
        return login_user(data, db)
    finally:
        db.close()

@router.post("/register")
def register(user: RegisterUser):
    db = SessionLocal()
    try:
        novo_usuario = criar_usuario(user, db)
        return {"message": "Usuário criado", "id": novo_usuario.id}
    finally:
        db.close()
    

@router.post("/refresh-token")
def refresh(data: RefreshToken):
    db = SessionLocal()
    try:
        refresh_t = refresh_token(data.token, db)
        return {"message": "Novo token gerado", "token" : refresh_t}
    finally:
        db.close()