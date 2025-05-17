import abc
from typing import List, Optional

# Importamos la Entidad de Dominio Corredor
from src.features.corredores.domain.entities import Corredor


class ICorredorRepository(abc.ABC):
    """Interfaz Abstracta para el Repositorio de Corredores."""

    @abc.abstractmethod
    def add(self, corredor: Corredor):
        """Añade un nuevo corredor al repositorio."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, corredor_id: int) -> Optional[Corredor]:
        """Obtiene un corredor por su ID técnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_numero(self, numero: int) -> Optional[Corredor]:
        """Obtiene un corredor por su número (identificador de negocio)."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_documento(self, documento: str) -> Optional[Corredor]:
        """Obtiene un corredor por su número de documento."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> Optional[Corredor]:
        """Obtiene un corredor por su dirección de correo electrónico."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[Corredor]:
        """Obtiene todos los corredores."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, corredor: Corredor):
        """Actualiza un corredor existente."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, corredor_id: int):
        """Elimina un corredor por su ID técnico."""
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, query: str = None, esta_activo: bool = None) -> List[Corredor]:
        """Busca corredores según criterios específicos."""
        raise NotImplementedError


import abc
from datetime import date
from typing import List, Optional, Dict, Any
from uuid import UUID

# Importamos las Entidades de Dominio
from src.features.corredores.domain.entities import Corredor, ClienteCorredor


class IClienteCorredorRepository(abc.ABC):
    """Interfaz para el Repositorio de la relación Cliente-Corredor."""
    
    @abc.abstractmethod
    def get_by_cliente_corredor(self, cliente_id: UUID, corredor_numero: int) -> Optional[ClienteCorredor]:
        """
        Obtiene una asignación específica entre un cliente y un corredor.
        
        Args:
            cliente_id: ID del cliente
            corredor_numero: Número del corredor
            
        Returns:
            ClienteCorredor si se encuentra, None en caso contrario
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_by_cliente(self, cliente_id: UUID) -> List[ClienteCorredor]:
        """
        Obtiene todas las asignaciones para un cliente específico.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Lista de asignaciones ClienteCorredor
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_by_corredor(self, corredor_numero: int) -> List[ClienteCorredor]:
        """
        Obtiene todas las asignaciones para un corredor específico.
        
        Args:
            corredor_numero: Número del corredor
            
        Returns:
            Lista de asignaciones ClienteCorredor
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def add(self, cliente_id: UUID, corredor_numero: int, fecha_asignacion: date) -> ClienteCorredor:
        """
        Agrega una nueva asignación entre un cliente y un corredor.
        
        Args:
            cliente_id: ID del cliente a asignar
            corredor_numero: Número del corredor al que se asignará el cliente
            fecha_asignacion: Fecha en que se realiza la asignación
            
        Returns:
            La entidad ClienteCorredor creada
            
        Raises:
            ClienteCorredorAsignacionDuplicadaException: Si ya existe una asignación para este par cliente-corredor
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def remove(self, cliente_id: UUID, corredor_numero: int) -> bool:
        """
        Elimina una asignación entre un cliente y un corredor.
        
        Args:
            cliente_id: ID del cliente
            corredor_numero: Número del corredor
            
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def update(self, cliente_id: UUID, corredor_numero_antiguo: int, 
              corredor_numero_nuevo: int, fecha_asignacion: date) -> ClienteCorredor:
        """
        Actualiza una asignación de cliente entre corredores.
        
        Args:
            cliente_id: ID del cliente a reasignar
            corredor_numero_antiguo: Número del corredor actual
            corredor_numero_nuevo: Número del nuevo corredor
            fecha_asignacion: Nueva fecha de asignación
            
        Returns:
            La entidad ClienteCorredor actualizada
            
        Raises:
            ClienteCorredorNoEncontradoException: Si no existe la asignación original
            ClienteCorredorAsignacionDuplicadaException: Si ya existe una asignación para el nuevo par cliente-corredor
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def exists(self, cliente_id: UUID, corredor_numero: int) -> bool:
        """
        Verifica si existe una asignación entre un cliente y un corredor.
        
        Args:
            cliente_id: ID del cliente
            corredor_numero: Número del corredor
            
        Returns:
            True si existe la asignación, False en caso contrario
        """
        raise NotImplementedError
