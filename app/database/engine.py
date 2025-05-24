from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()
metadata = Base.metadata
senha_banco = os.getenv("SENHA_BANCO_POSTGRES")

engine = create_engine(f"postgresql+psycopg2://postgres:{senha_banco}@localhost:5432/luestilo")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
