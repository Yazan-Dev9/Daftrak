import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database.connection import db

Base = db.get_base()


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")

    def __repr__(self):
        return f"<Sale(product_id={self.product_id}, customer_id={self.customer_id}, quantity={self.quantity}, price={self.price})>"
