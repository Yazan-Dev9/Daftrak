import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from database.connection import db

Base = db.get_base()


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    month = Column(String(100), nullable=True)
    total = Column(Float, nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f"<Report(name={self.name}, month={self.month}, total={self.total})>"
