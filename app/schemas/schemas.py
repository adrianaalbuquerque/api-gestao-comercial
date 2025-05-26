from pydantic import BaseModel

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
