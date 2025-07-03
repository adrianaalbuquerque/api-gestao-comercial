from pydantic import BaseModel
from typing import List, Optional
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
    cpf: str
    email: str
    name: str

    model_config = {
        "from_attributes": True
    }

class Product(BaseModel):
    descricao: str
    valor_venda: Decimal
    codigo_barras: str
    secao: Optional[str] = None
    estoque: int
    data_validade: Optional[date] = None
    imagens: Optional[str] = None

class ProdutoQuantidade(BaseModel):
    id: int
    quantidade: int
    
class Orders(BaseModel):
    period: date
    status: str
    client_id: int
    product_quantity: List[ProdutoQuantidade]
