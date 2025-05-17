"""Módulo de corredores.

Este módulo proporciona funcionalidades para gestionar corredores de seguros,
incluyendo su asignación a clientes y otras operaciones relacionadas.
"""

# Exportar componentes principales
from .application.dtos_cliente_corredor import (
    AsignarClienteCorredorCommand,
    ClienteCorredorDto,
    ReasignarClienteCommand,
)
from .application.interfaces.repositories import IClienteCorredorRepository, ICorredorRepository
from .application.use_cases_cliente_corredor import (
    AsignarClienteCorredorUseCase,
    EliminarAsignacionClienteCorredorUseCase,
    ListarClientesPorCorredorUseCase,
    ListarCorredoresPorClienteUseCase,
    ReasignarClienteUseCase,
)

# Exportar dependencias
from .dependencies import get_cliente_corredor_repository, get_corredor_repository
from .infrastructure.repositories import SQLAlchemyCorredorRepository
from .infrastructure.repositories_cliente_corredor import SQLAlchemyClienteCorredorRepository

__all__ = [
    # DTOs
    'ClienteCorredorDto',
    'AsignarClienteCorredorCommand',
    'ReasignarClienteCommand',
    
    # Casos de uso
    'AsignarClienteCorredorUseCase',
    'ReasignarClienteUseCase',
    'EliminarAsignacionClienteCorredorUseCase',
    'ListarClientesPorCorredorUseCase',
    'ListarCorredoresPorClienteUseCase',
    
    # Interfaces
    'IClienteCorredorRepository',
    'ICorredorRepository',
    
    # Implementaciones
    'SQLAlchemyClienteCorredorRepository',
    'SQLAlchemyCorredorRepository',
    
    # Dependencias
    'get_corredor_repository',
    'get_cliente_corredor_repository'
]
