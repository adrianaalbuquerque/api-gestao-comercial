from sqlalchemy import Column, ForeignKey, Integer
from database.engine import Base

class OrdersProducts(Base):
    __tablename__ = "orders_products"

    orders_products_id = Column(Integer, primary_key=True, autoincrement=True)
    orders_id = Column(Integer, ForeignKey("orders.id"))
    products_id = Column(Integer, ForeignKey("products.id"))
    product_qntd = Column(Integer)
