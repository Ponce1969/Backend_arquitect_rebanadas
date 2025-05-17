# Este archivo permite que el directorio sea un paquete Python

from .repositories import (
    ICorredorRepository,
    IClienteCorredorRepository
)

__all__ = [
    'ICorredorRepository',
    'IClienteCorredorRepository'
]
