from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from database.engine import Base

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    client_cpf = Column(String(14),  unique=True, nullable=False)
    client_email = Column(String(100), unique=True, nullable=False)
    client_name = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"))

    usuario = relationship("User", back_populates="clientes")

