# Este archivo permite que el directorio sea un paquete Python

from .repositories import IClienteCorredorRepository, ICorredorRepository

__all__ = [
    'ICorredorRepository',
    'IClienteCorredorRepository'
]
