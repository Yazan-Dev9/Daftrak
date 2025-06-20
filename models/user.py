import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from database.connection import db

Base = db.get_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    birth_date = Column(Date, nullable=True)
    email = Column(String(120), unique=True, nullable=True)
    password = Column(String(128), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    role = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
