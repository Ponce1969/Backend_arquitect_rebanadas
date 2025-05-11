import abc
import uuid
from typing import List, Optional
from datetime import date

# Importamos la Entidad de Dominio Cliente
from src.features.clientes.domain.entities import Cliente


class AbstractClienteRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Clientes."""

    @abc.abstractmethod
    def add(self, cliente: Cliente):
        """Añade un nuevo cliente al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, cliente_id: uuid.UUID) -> Optional[Cliente]:
        """Obtiene un cliente por su ID técnico (UUID)."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_numero_cliente(self, numero_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su número de cliente (identificador de negocio)."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_documento(self, tipo_documento_id: int, numero_documento: str) -> Optional[Cliente]:
        """Obtiene un cliente por su tipo y número de documento."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[Cliente]:
        """Obtiene un cliente por su dirección de correo electrónico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, cliente: Cliente):
        """Actualiza un cliente existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, cliente_id: uuid.UUID):
        """Elimina un cliente por su ID técnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, query: str = None, tipo_documento_id: int = None, localidad: str = None) -> List[Cliente]:
        """Busca clientes según criterios específicos."""
        raise NotImplementedError
