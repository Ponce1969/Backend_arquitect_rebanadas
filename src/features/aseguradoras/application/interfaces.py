import abc

from ..domain.entities import Aseguradora


class AbstractAseguradoraRepository(abc.ABC):
    """Interfaz abstracta para el repositorio de Aseguradoras."""

    @abc.abstractmethod
    def add(self, aseguradora: Aseguradora) -> Aseguradora:
        """Añade una nueva aseguradora al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, aseguradora_id: int) -> Aseguradora | None:
        """Obtiene una aseguradora por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> list[Aseguradora]:
        """Obtiene todas las aseguradoras."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, aseguradora: Aseguradora) -> Aseguradora:
        """Actualiza una aseguradora existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, aseguradora_id: int) -> bool:
        """Elimina una aseguradora por su ID."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_nombre(self, nombre: str) -> Aseguradora | None:
        """Obtiene una aseguradora por su nombre."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_identificador_fiscal(self, identificador_fiscal: str) -> Aseguradora | None:
        """Obtiene una aseguradora por su identificador fiscal."""
        raise NotImplementedError
