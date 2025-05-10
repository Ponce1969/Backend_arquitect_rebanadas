from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings

# Convertir la URL de conexión a string si es necesario
database_url = str(settings.SQLALCHEMY_DATABASE_URI)

# Crear el motor de SQLAlchemy
engine = create_engine(
    database_url,
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependencia para obtener una sesión de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
