import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.connection import db

Base = db.get_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    made_date = Column(DateTime, nullable=True)
    exp_date = Column(DateTime, nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    sales = relationship("Sale", back_populates="product")
    purchases = relationship("Purchase", back_populates="product")

    def __repr__(self):
        return f"<Product(name={self.name}, category={self.category}, quantity={self.quantity}, price={self.price}, cost={self.cost})>"
