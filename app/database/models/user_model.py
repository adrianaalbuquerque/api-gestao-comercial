from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from database.engine import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(200), unique=True, nullable=False)
    user_tipo = Column(String(1), nullable=False)
    user_senha = Column(String(255), nullable=False)

    clientes = relationship("Client", back_populates="usuario")

