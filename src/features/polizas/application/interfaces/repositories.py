import abc
import uuid
from typing import List, Optional
from datetime import date

# Importamos la Entidad de Dominio Poliza
from src.features.polizas.domain.entities import Poliza


class AbstractPolizaRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Pu00f3lizas."""

    @abc.abstractmethod
    def add(self, poliza: Poliza):
        """Au00f1ade una nueva pu00f3liza al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, poliza_id: int) -> Optional[Poliza]:
        """Obtiene una pu00f3liza por su ID tu00e9cnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_numero_poliza(self, numero_poliza: str, carpeta: Optional[str] = None) -> Optional[Poliza]:
        """Obtiene una pu00f3liza por su nu00famero y carpeta (identificador de negocio)."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Poliza]:
        """Obtiene todas las pu00f3lizas."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, poliza: Poliza):
        """Actualiza una pu00f3liza existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, poliza_id: int):
        """Elimina una pu00f3liza por su ID tu00e9cnico."""
        raise NotImplementedError

    # Mu00e9todos de bu00fasqueda especu00edficos
    @abc.abstractmethod
    def get_by_cliente(self, cliente_id: uuid.UUID) -> List[Poliza]:
        """Obtiene todas las pu00f3lizas de un cliente especu00edfico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_vigentes_by_cliente(self, cliente_id: uuid.UUID, today: date) -> List[Poliza]:
        """Obtiene las pu00f3lizas vigentes de un cliente a una fecha dada."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_corredor(self, corredor_id: int) -> List[Poliza]:
        """Obtiene todas las pu00f3lizas de un corredor especu00edfico."""
        raise NotImplementedError
