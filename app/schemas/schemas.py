from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class LoginData(BaseModel):
    user_email: str
    senha: str

class RegisterUser(BaseModel):
    username: str
    email: str
    tipo: str
    senha: str

class RefreshToken(BaseModel):
    token: str

class Clientes(BaseModel):
    client_cpf: str
    client_email: str
    client_name: str

    model_config = {
        "from_attributes": True
    }

class Product(BaseModel):
    descricao: str
    valor_venda: Decimal
    codigo_barras: str
    secao: Optional[str] = None
    estoque_inicial: int
    data_validade: Optional[date] = None
    imagens: Optional[str] = None

    model_config = {
        "from_attributes": True
    }