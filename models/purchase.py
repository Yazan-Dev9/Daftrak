import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from database.connection import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = db.get_base()


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    debt = Column(Float, nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="purchases")
    supplier = relationship("Supplier", back_populates="purchases")

    def __repr__(self):
        return f"<Purchase(product_id={self.product_id}, supplier_id={self.supplier_id}, quantity={self.quantity}, price={self.price}, total={self.total})>"