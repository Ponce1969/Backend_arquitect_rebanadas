"""Módulo de corredores.

Este módulo proporciona funcionalidades para gestionar corredores de seguros,
incluyendo su asignación a clientes y otras operaciones relacionadas.
"""

# Exportar componentes principales
from .application.dtos_cliente_corredor import (
    ClienteCorredorDto,
    AsignarClienteCorredorCommand,
    ReasignarClienteCommand
)

from .application.use_cases_cliente_corredor import (
    AsignarClienteCorredorUseCase,
    ReasignarClienteUseCase,
    EliminarAsignacionClienteCorredorUseCase,
    ListarClientesPorCorredorUseCase,
    ListarCorredoresPorClienteUseCase
)

from .application.interfaces.repositories import (
    IClienteCorredorRepository,
    ICorredorRepository
)

from .infrastructure.repositories_cliente_corredor import SQLAlchemyClienteCorredorRepository
from .infrastructure.repositories import SQLAlchemyCorredorRepository

# Exportar dependencias
from .dependencies import (
    get_corredor_repository,
    get_cliente_corredor_repository
)

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
