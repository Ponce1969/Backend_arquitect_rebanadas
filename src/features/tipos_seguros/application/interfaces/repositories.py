import abc
from typing import List, Optional

# Importamos la Entidad de Dominio TipoSeguro
from src.features.tipos_seguros.domain.entities import TipoSeguro

class AbstractTipoSeguroRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Tipos de Seguro."""

    @abc.abstractmethod
    def add(self, tipo_seguro: TipoSeguro):
        """Añade un nuevo tipo de seguro al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, tipo_seguro_id: int) -> Optional[TipoSeguro]:
        """Obtiene un tipo de seguro por su ID técnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[TipoSeguro]:
        """Obtiene un tipo de seguro por su código."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[TipoSeguro]:
        """Obtiene todos los tipos de seguro."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, tipo_seguro: TipoSeguro):
        """Actualiza un tipo de seguro existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, tipo_seguro_id: int):
        """Elimina un tipo de seguro por su ID técnico."""
        raise NotImplementedError

    # Método para obtener tipos de seguro por aseguradora
    @abc.abstractmethod
    def get_by_aseguradora(self, aseguradora_id: int) -> List[TipoSeguro]:
        """Obtiene tipos de seguro asociados a una aseguradora específica."""
        raise NotImplementedError
