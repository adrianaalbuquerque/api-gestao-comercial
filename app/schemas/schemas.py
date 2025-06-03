from pydantic import BaseModel, Field

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
