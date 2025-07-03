from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, Text
from database.engine import Base
from sqlalchemy.orm import relationship

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    valor_venda = Column(Numeric(10, 2), nullable=False)  
    codigo_barras = Column(String(50), unique=True, nullable=False)
    secao = Column(String(100), nullable=True) 
    estoque = Column(Integer, nullable=False, default=0)
    data_validade = Column(Date, nullable=True)
    imagens = Column(Text, nullable=True)