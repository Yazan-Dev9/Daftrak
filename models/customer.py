from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from database.connection import db

Base = db.get_base()


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(120), unique=True, nullable=True)
    address = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    debts = relationship("Debt", back_populates="customer")
    sales = relationship("Sale", back_populates="customer")

    def __repr__(self):
        return f"<Customer(name={self.name}, phone={self.phone}, email={self.email}, address={self.address})>"