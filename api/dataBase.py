from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL do banco de dados
URL_DATABASE = 'sqlite:///./Users.db'

# Criação do engine para o banco de dados
engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos
Base = declarative_base()
