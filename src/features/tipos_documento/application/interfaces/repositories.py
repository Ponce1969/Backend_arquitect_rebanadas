from abc import ABC, abstractmethod
from typing import List, Optional

from src.features.tipos_documento.domain.entities import TipoDocumento


class AbstractTipoDocumentoRepository(ABC):
    """Interfaz abstracta para el repositorio de TipoDocumento."""
    
    @abstractmethod
    def get_by_id(self, tipo_id: int) -> Optional[TipoDocumento]:
        """Obtiene un tipo de documento por su ID."""
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[TipoDocumento]:
        """Obtiene un tipo de documento por su cu00f3digo."""
        pass
    
    @abstractmethod
    def get_default(self) -> Optional[TipoDocumento]:
        """Obtiene el tipo de documento marcado como default."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[TipoDocumento]:
        """Obtiene todos los tipos de documento activos."""
        pass
    
    @abstractmethod
    def add(self, tipo: TipoDocumento) -> TipoDocumento:
        """Agrega un nuevo tipo de documento."""
        pass
    
    @abstractmethod
    def update(self, tipo: TipoDocumento) -> TipoDocumento:
        """Actualiza un tipo de documento existente."""
        pass
    
    @abstractmethod
    def delete(self, tipo_id: int) -> bool:
        """Elimina un tipo de documento (marcu00e1ndolo como inactivo)."""
        pass
