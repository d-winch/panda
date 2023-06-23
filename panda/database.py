from sqlalchemy import create_engine

#from sqlalchemy.ext.declarative import as_declarative, declarative_base, declared_attr
from sqlalchemy.orm import declarative_base, sessionmaker

from panda.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # check_same_thread required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
