from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings
from src.infrastructure.database.base import Base  # Re-exportar Base para que otros módulos puedan importarlo desde aquí

__all__ = ['Base', 'get_db', 'SessionLocal', 'engine']

# Crear el motor de SQLAlchemy
engine = create_engine(
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# Crear una clase de sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
