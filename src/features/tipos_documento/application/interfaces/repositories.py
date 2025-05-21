from abc import abstractmethod
from typing import List, Optional

from src.features.shared.interfaces.repositories import AbstractBaseRepository
from src.features.tipos_documento.domain.entities import TipoDocumento


class AbstractTipoDocumentoRepository(AbstractBaseRepository[TipoDocumento]):
    """Interfaz abstracta para el repositorio de TipoDocumento."""
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[TipoDocumento]:
        """Obtiene un tipo de documento por su ID.
        
        Args:
            entity_id: El ID del tipo de documento a buscar.
            
        Returns:
            El tipo de documento encontrado o None si no existe.
        """
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[TipoDocumento]:
        """Obtiene un tipo de documento por su codigo."""
        pass
    
    @abstractmethod
    def get_default(self) -> Optional[TipoDocumento]:
        """Obtiene el tipo de documento marcado como default."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[TipoDocumento]:
        """Obtiene todos los tipos de documento activos, con soporte para paginación.
        
        Args:
            skip: Número de registros a omitir (para paginación).
            limit: Número máximo de registros a devolver (para paginación).
            
        Returns:
            Lista de tipos de documento encontrados.
        """
        pass
    
    @abstractmethod
    def add(self, entity: TipoDocumento) -> TipoDocumento:
        """Agrega un nuevo tipo de documento."""
        pass
    
    @abstractmethod
    def update(self, entity: TipoDocumento) -> TipoDocumento:
        """Actualiza un tipo de documento existente."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Elimina un tipo de documento (marcándolo como inactivo).
        
        Args:
            entity_id: El ID del tipo de documento a eliminar.
        """
        pass
