import abc
from typing import Optional, List
from uuid import UUID

from ..domain.entities import Cliente


class AbstractClienteRepository(abc.ABC):
    """Interfaz abstracta para el repositorio de Clientes."""

    @abc.abstractmethod
    def add(self, cliente: Cliente) -> Cliente:
        """Añade un nuevo cliente al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, cliente_id: UUID) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_numero_cliente(self, numero_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su número de cliente."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_numero_documento(self, numero_documento: str) -> Optional[Cliente]:
        """Obtiene un cliente por su número de documento."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[Cliente]:
        """Obtiene un cliente por su email."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, cliente: Cliente) -> Cliente:
        """Actualiza un cliente existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, cliente_id: UUID) -> bool:
        """Elimina un cliente por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, query: str) -> List[Cliente]:
        """Busca clientes que coincidan con la consulta en nombres, apellidos o número de documento."""
        raise NotImplementedError
