from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


class DatabaseConnection:
    def __init__(self, db_url: str = "sqlite:///mydb.db"):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = declarative_base()

    def get_engine(self):
        return self.engine

    def get_session(self) -> Session:
        return self.SessionLocal()

    def get_base(self):
        return self.Base

    def init_db(self):
        self.Base.metadata.create_all(bind=self.engine)


db = DatabaseConnection()
