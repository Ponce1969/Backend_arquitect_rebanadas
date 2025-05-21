from abc import abstractmethod
from typing import List, Optional

from src.features.shared.interfaces.repositories import AbstractBaseRepository
from src.features.monedas.domain.entities import Moneda


class AbstractMonedaRepository(AbstractBaseRepository[Moneda]):
    """Interfaz abstracta para el repositorio de Moneda."""
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Moneda]:
        """Obtiene una moneda por su ID.
        
        Args:
            entity_id: El ID de la moneda a buscar.
            
        Returns:
            La moneda encontrada o None si no existe.
        """
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Moneda:
        """Obtiene una moneda por su codigo."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Moneda]:
        """Obtiene todas las monedas activas, con soporte para paginacion.
        
        Args:
            skip: Numero de registros a omitir (para paginacion).
            limit: Numero maximo de registros a devolver (para paginacion).
            
        Returns:
            Lista de monedas encontradas.
        """
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
    def delete(self, entity_id: int) -> None:
        """Elimina una moneda (marcandola como inactiva).
        
        Args:
            entity_id: El ID de la moneda a eliminar.
        """
        pass
