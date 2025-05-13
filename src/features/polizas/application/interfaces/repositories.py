import abc
import uuid
from typing import List, Optional
from datetime import date

# Importamos la Entidad de Dominio Poliza
from src.features.polizas.domain.entities import Poliza


class AbstractPolizaRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Polizas."""

    @abc.abstractmethod
    def add(self, poliza: Poliza):
        """Añade una nueva poliza al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, poliza_id: int) -> Optional[Poliza]:
        """Obtiene una poliza por su ID técnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_numero_poliza(self, numero_poliza: str, carpeta: Optional[str] = None) -> Optional[Poliza]:
        """Obtiene una poliza por su número y carpeta (identificador de negocio)."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Poliza]:
        """Obtiene todas las polizas."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, poliza: Poliza):
        """Actualiza una poliza existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, poliza_id: int):
        """Elimina una poliza por su ID técnico."""
        raise NotImplementedError

    # Métodos de búsqueda específicos
    @abc.abstractmethod
    def get_by_cliente(self, cliente_id: uuid.UUID) -> List[Poliza]:
        """Obtiene todas las polizas de un cliente especifico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_vigentes_by_cliente(self, cliente_id: uuid.UUID, today: date) -> List[Poliza]:
        """Obtiene las polizas vigentes de un cliente a una fecha dada."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_corredor(self, corredor_id: int) -> List[Poliza]:
        """Obtiene todas las polizas de un corredor especifico."""
        raise NotImplementedError
