from sqlalchemy import Column, Integer, String
from database.engine import Base

class User(Base):
    __tablename__ = "clients"

    client_cpf = Column(String(14),  primary_key=True, nullable=False)
    client_email = Column(String(100), unique=True, nullable=False)
    client_name = Column(String(100), nullable=False)
    id = Column(Integer, autoincrement=True)
