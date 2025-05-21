from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

# Define un TypeVar para representar el tipo de entidad con el que trabaja el repositorio
T = TypeVar('T')

class AbstractBaseRepository(ABC, Generic[T]):
    """Interfaz base generic para repositorios.
    
    Esta interfaz define las operaciones CRUD basicas que deben implementar
    todos los repositorios. Cada repositorio especifico debe extender esta interfaz
    y proporcionar implementaciones concretas para estos metodos, asi como
    metodos adicionales especificos para su dominio si es necesario.
    """
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Agrega una nueva entidad al repositorio.
        
        Args:
            entity: La entidad a agregar.
            
        Returns:
            La entidad agregada, posiblemente con campos actualizados (como ID).
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Obtiene una entidad por su ID.
        
        Args:
            entity_id: El ID de la entidad a buscar.
            
        Returns:
            La entidad encontrada o None si no existe.
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Actualiza una entidad existente.
        
        Args:
            entity: La entidad con los datos actualizados.
            
        Returns:
            La entidad actualizada.
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Elimina una entidad por su ID.
        
        Args:
            entity_id: El ID de la entidad a eliminar.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene todas las entidades, con soporte para paginaciu00f3n.
        
        Args:
            skip: Nu00famero de registros a omitir (para paginaciu00f3n).
            limit: Nu00famero mu00e1ximo de registros a devolver (para paginaciu00f3n).
            
        Returns:
            Lista de entidades encontradas.
        """
        pass
