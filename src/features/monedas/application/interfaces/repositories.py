from abc import ABC, abstractmethod
from typing import List, Optional

from src.features.monedas.domain.entities import Moneda


class AbstractMonedaRepository(ABC):
    """Interfaz abstracta para el repositorio de Moneda."""
    
    @abstractmethod
    def get_by_id(self, moneda_id: int) -> Moneda:
        """Obtiene una moneda por su ID."""
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Moneda:
        """Obtiene una moneda por su cu00f3digo."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Moneda]:
        """Obtiene todas las monedas activas."""
        pass
    
    @abstractmethod
    def add(self, moneda: Moneda) -> Moneda:
        """Agrega una nueva moneda."""
        pass
    
    @abstractmethod
    def update(self, moneda: Moneda) -> Moneda:
        """Actualiza una moneda existente."""
        pass
    
    @abstractmethod
    def delete(self, moneda_id: int) -> bool:
        """Elimina una moneda (marcu00e1ndola como inactiva)."""
        pass
