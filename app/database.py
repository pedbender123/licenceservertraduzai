from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Aponte o caminho do DB para dentro da pasta /app
DATABASE_URL = "sqlite:////app/licenses.db" 

# ... (resto do arquivo sem alterações) ...
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()