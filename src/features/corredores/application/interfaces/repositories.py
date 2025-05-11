import abc
from typing import List, Optional

# Importamos la Entidad de Dominio Corredor
from src.features.corredores.domain.entities import Corredor


class AbstractCorredorRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Corredores."""

    @abc.abstractmethod
    def add(self, corredor: Corredor):
        """Au00f1ade un nuevo corredor al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, corredor_id: int) -> Optional[Corredor]:
        """Obtiene un corredor por su ID tu00e9cnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_numero(self, numero: int) -> Optional[Corredor]:
        """Obtiene un corredor por su nu00famero (identificador de negocio)."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_documento(self, documento: str) -> Optional[Corredor]:
        """Obtiene un corredor por su nu00famero de documento."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[Corredor]:
        """Obtiene un corredor por su direcciu00f3n de correo electru00f3nico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Corredor]:
        """Obtiene todos los corredores."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, corredor: Corredor):
        """Actualiza un corredor existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, corredor_id: int):
        """Elimina un corredor por su ID tu00e9cnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, query: str = None, esta_activo: bool = None) -> List[Corredor]:
        """Busca corredores segu00fan criterios especu00edficos."""
        raise NotImplementedError
