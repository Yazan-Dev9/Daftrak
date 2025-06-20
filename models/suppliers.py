import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from database.connection import db

Base = db.get_base()


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(120), unique=True, nullable=True)
    address = Column(String(255), nullable=True)
    payable = Column(Float, nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    purchases = relationship("Purchase", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(name={self.name}, phone={self.phone}, email={self.email}, address={self.address})>"
