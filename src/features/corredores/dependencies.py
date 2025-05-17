"""Módulo de dependencias para el módulo de corredores."""
from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.features.clientes.application.interfaces.repositories import IClienteRepository
from src.features.clientes.infrastructure.repositories import SQLAlchemyClienteRepository
from src.features.corredores.application.interfaces import (
    IClienteCorredorRepository,
    ICorredorRepository,
)
from src.features.corredores.infrastructure.repositories import SQLAlchemyCorredorRepository
from src.features.corredores.infrastructure.repositories_cliente_corredor import (
    SQLAlchemyClienteCorredorRepository,
)
from src.infrastructure.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Obtiene una sesión de base de datos.
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_corredor_repository(db: Session = Depends(get_db)) -> ICorredorRepository:
    """Obtiene una instancia del repositorio de corredores.
    
    Args:
        db: Sesión de base de datos inyectada por FastAPI
        
    Returns:
        ICorredorRepository: Implementación del repositorio de corredores
    """
    return SQLAlchemyCorredorRepository(db)


def get_cliente_repository(db: Session = Depends(get_db)) -> IClienteRepository:
    """Obtiene una instancia del repositorio de clientes.
    
    Args:
        db: Sesión de base de datos inyectada por FastAPI
        
    Returns:
        IClienteRepository: Implementación del repositorio de clientes
    """
    return SQLAlchemyClienteRepository(db)


def get_cliente_corredor_repository(
    db: Session = Depends(get_db)
) -> IClienteCorredorRepository:
    """Obtiene una instancia del repositorio de relaciones cliente-corredor.
    
    Args:
        db: Sesión de base de datos inyectada por FastAPI
        
    Returns:
        IClienteCorredorRepository: Implementación del repositorio de relaciones cliente-corredor
    """
    return SQLAlchemyClienteCorredorRepository(db)
