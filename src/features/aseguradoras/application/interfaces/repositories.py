import abc
from typing import List, Optional

# Importamos la Entidad de Dominio Aseguradora
from src.features.aseguradoras.domain.entities import Aseguradora


class AbstractAseguradoraRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Aseguradoras."""

    @abc.abstractmethod
    def add(self, aseguradora: Aseguradora):
        """Añade una nueva aseguradora al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, aseguradora_id: int) -> Optional[Aseguradora]:
        """Obtiene una aseguradora por su ID técnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Aseguradora]:
        """Obtiene una aseguradora por su nombre."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_identificador_fiscal(self, identificador_fiscal: str) -> Optional[Aseguradora]:
        """Obtiene una aseguradora por su identificador fiscal."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Aseguradora]:
        """Obtiene todas las aseguradoras."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, aseguradora: Aseguradora):
        """Actualiza una aseguradora existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, aseguradora_id: int):
        """Elimina una aseguradora por su ID técnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, query: str = None, esta_activa: bool = None) -> List[Aseguradora]:
        """Busca aseguradoras según criterios específicos."""
        raise NotImplementedError
