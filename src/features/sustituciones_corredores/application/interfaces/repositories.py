import abc
from datetime import date
from typing import List, Optional

from src.features.sustituciones_corredores.domain.entities import SustitucionCorredor


class AbstractSustitucionCorredorRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Sustituciones de Corredores."""

    @abc.abstractmethod
    def add(self, sustitucion: SustitucionCorredor) -> SustitucionCorredor:
        """Au00f1ade una nueva sustituciu00f3n de corredor al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, sustitucion_id: int) -> Optional[SustitucionCorredor]:
        """Obtiene una sustituciu00f3n por su ID tu00e9cnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_corredor_ausente(self, corredor_numero: int) -> List[SustitucionCorredor]:
        """Obtiene todas las sustituciones donde el corredor especificado estu00e1 ausente."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_corredor_sustituto(self, corredor_numero: int) -> List[SustitucionCorredor]:
        """Obtiene todas las sustituciones donde el corredor especificado es sustituto."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_activas_by_corredor_ausente(self, corredor_numero: int, fecha_actual: date = None) -> List[SustitucionCorredor]:
        """Obtiene las sustituciones activas donde el corredor especificado estu00e1 ausente."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_activas_by_corredor_sustituto(self, corredor_numero: int, fecha_actual: date = None) -> List[SustitucionCorredor]:
        """Obtiene las sustituciones activas donde el corredor especificado es sustituto."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[SustitucionCorredor]:
        """Obtiene todas las sustituciones de corredores."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_activas(self, fecha_actual: date = None) -> List[SustitucionCorredor]:
        """Obtiene todas las sustituciones activas en la fecha actual."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, sustitucion: SustitucionCorredor) -> SustitucionCorredor:
        """Actualiza una sustituciu00f3n existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, sustitucion_id: int) -> None:
        """Elimina una sustituciu00f3n por su ID tu00e9cnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def finalizar(self, sustitucion_id: int, fecha_fin: date = None) -> SustitucionCorredor:
        """Finaliza una sustituciu00f3n estableciendo su fecha de fin y cambiando su estado a inactiva."""
        raise NotImplementedError
