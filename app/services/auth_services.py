from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database.engine import SessionLocal
from database.models.user_model import User
from sqlalchemy.exc import IntegrityError
from schemas.schemas import LoginData, RegisterUser
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

JWT_SECRET = os.getenv("JWT_SECRET")
print(repr(JWT_SECRET))

def token_payload(user, minutes=45):
    now = datetime.utcnow()
    return {
        "user_id": user.id,
        "user_email": user.user_email,
        "user_tipo" : user.user_tipo,
        "iss": "Adriana",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }

def generate_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def login_user(data: LoginData, db: Session): #gera o acess token    
    user = db.query(User).filter_by(user_email=data.user_email).first()
    if not user or not verify_password(data.senha, user.user_senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    payload = token_payload(user, 45)
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"token": token}

def criar_usuario(data: RegisterUser, db: Session):
    novo_usuario = User(
        user_name=data.username,
        user_email=data.email,
        user_tipo=data.tipo,
        user_senha= generate_password_hash(data.senha)
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return novo_usuario
    except IntegrityError as e:
        db.rollback()
        if 'unique constraint' in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado"
            )
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário"
        )

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_exp": True}
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou fraudado")

def refresh_token(token: str, db: Session):
    try:
        payload = decode_token(token)
    except HTTPException as e:
        raise e  # Propaga erro

    exp = payload.get("exp")
    if not exp or datetime.utcnow().timestamp() > exp:
        print("Token expirado")

    if payload.get("iss") != "Adriana":
        raise HTTPException(status_code=401, detail="Issuer inválido")

    email = payload.get("user_email")
    if not email:
        raise HTTPException(status_code=401, detail="Email ausente no token")

    user = db.query(User).filter_by(user_email=email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    payload_token = token_payload(user, 45)
    new_token = jwt.encode(payload_token, JWT_SECRET, algorithm="HS256")
    return new_token

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: ID ausente",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return user

def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.user_tipo != "A":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar esta ação."
        )
    return current_user
