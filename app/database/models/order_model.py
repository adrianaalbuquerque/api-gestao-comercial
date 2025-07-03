from sqlalchemy import Column, Date, ForeignKey, Integer, String
from database.engine import Base
from sqlalchemy.orm import relationship

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(Date, nullable=False)
    status = Column(String(100), nullable=False)
    id_client = Column(Integer, ForeignKey("clients.client_id"))
