from datetime import date
from typing import List
from uuid import UUID

from src.features.corredores.application.dtos_cliente_corredor import (
    ClienteCorredorDto,
    AsignarClienteCorredorCommand,
    ReasignarClienteCommand
)
from src.features.corredores.domain.entities import ClienteCorredor as ClienteCorredorEntity
from src.features.corredores.domain.exceptions import (
    ClienteNoEncontradoException,
    CorredorNoEncontradoException,
    ClienteCorredorAsignacionDuplicadaException,
    ClienteCorredorNoEncontradoException,
    FechaAsignacionInvalidaException
)
from src.features.corredores.application.interfaces.repositories import IClienteCorredorRepository
from src.features.clientes.application.interfaces.repositories import IClienteRepository
from src.features.corredores.application.interfaces.repositories import ICorredorRepository


class AsignarClienteCorredorUseCase:
    """Caso de uso para asignar un cliente a un corredor."""
    
    def __init__(self, cliente_repository, corredor_repository, cliente_corredor_repository):
        self.cliente_repository = cliente_repository
        self.corredor_repository = corredor_repository
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, command: AsignarClienteCorredorCommand) -> ClienteCorredorDto:
        """
        Asigna un cliente a un corredor.
        
        Args:
            command: Comando con los datos necesarios para la asignación
            
        Returns:
            ClienteCorredorDto: DTO con los datos de la asignación creada
            
        Raises:
            ClienteNoEncontradoException: Si no se encuentra el cliente
            CorredorNoEncontradoException: Si no se encuentra el corredor
            ClienteCorredorAsignacionDuplicadaException: Si ya existe una asignación para el par cliente-corredor
            FechaAsignacionInvalidaException: Si la fecha de asignación es futura
        """
        # Validar que la fecha de asignación no sea futura
        fecha_asignacion = command.fecha_asignacion or date.today()
        
        # Verificar que el cliente existe (el repositorio lanzará la excepción si no existe)
        cliente = self.cliente_repository.get_by_id(command.cliente_id)
        if not cliente:
            raise ClienteNoEncontradoException(command.cliente_id)
        
        # Verificar que el corredor existe (el repositorio lanzará la excepción si no existe)
        corredor = self.corredor_repository.get_by_numero(command.corredor_numero)
        if not corredor:
            raise CorredorNoEncontradoException(command.corredor_numero)
        
        try:
            # Intentar crear la asignación
            asignacion = self.cliente_corredor_repository.add(
                cliente_id=command.cliente_id,
                corredor_numero=command.corredor_numero,
                fecha_asignacion=fecha_asignacion
            )
            
            # Convertir la entidad a DTO para la respuesta
            return ClienteCorredorDto(
                cliente_id=asignacion.cliente_id,
                corredor_numero=asignacion.corredor_numero,
                fecha_asignacion=asignacion.fecha_asignacion
            )
            
        except ClienteCorredorAsignacionDuplicadaException as e:
            # Relanzar la excepción con un mensaje más descriptivo
            raise ClienteCorredorAsignacionDuplicadaException(
                command.cliente_id, command.corredor_numero
            ) from e
        except FechaAsignacionInvalidaException as e:
            # Relanzar la excepción de fecha inválida
            raise FechaAsignacionInvalidaException(str(fecha_asignacion)) from e


class ReasignarClienteUseCase:
    """Caso de uso para reasignar un cliente de un corredor a otro."""
    
    def __init__(self, cliente_repository, corredor_repository, cliente_corredor_repository):
        self.cliente_repository = cliente_repository
        self.corredor_repository = corredor_repository
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, command: ReasignarClienteCommand) -> ClienteCorredorDto:
        """
        Reasigna un cliente de un corredor a otro.
        
        Args:
            command: Comando con los datos necesarios para la reasignación
            
        Returns:
            ClienteCorredorDto: DTO con los datos de la asignación actualizada
            
        Raises:
            ClienteNoEncontradoException: Si no se encuentra el cliente
            CorredorNoEncontradoException: Si no se encuentra el corredor antiguo o el nuevo
            ClienteCorredorNoEncontradoException: Si no existe la asignación original
            ClienteCorredorAsignacionDuplicadaException: Si ya existe una asignación para el nuevo par
            FechaAsignacionInvalidaException: Si la fecha de asignación es futura
        """
        # Validar que la fecha de asignación no sea futura
        fecha_asignacion = command.fecha_asignacion or date.today()
        
        # Verificar que el cliente existe
        cliente = self.cliente_repository.get_by_id(command.cliente_id)
        if not cliente:
            raise ClienteNoEncontradoException(command.cliente_id)
        
        # Verificar que el corredor antiguo existe
        corredor_antiguo = self.corredor_repository.get_by_numero(command.corredor_numero_antiguo)
        if not corredor_antiguo:
            raise CorredorNoEncontradoException(command.corredor_numero_antiguo)
        
        # Verificar que el nuevo corredor existe
        corredor_nuevo = self.corredor_repository.get_by_numero(command.corredor_numero_nuevo)
        if not corredor_nuevo:
            raise CorredorNoEncontradoException(command.corredor_numero_nuevo)
        
        try:
            # Actualizar la asignación
            asignacion_actualizada = self.cliente_corredor_repository.update(
                cliente_id=command.cliente_id,
                corredor_numero_antiguo=command.corredor_numero_antiguo,
                corredor_numero_nuevo=command.corredor_numero_nuevo,
                fecha_asignacion=fecha_asignacion
            )
            
            # Convertir la entidad a DTO para la respuesta
            return ClienteCorredorDto(
                cliente_id=asignacion_actualizada.cliente_id,
                corredor_numero=asignacion_actualizada.corredor_numero,
                fecha_asignacion=asignacion_actualizada.fecha_asignacion
            )
            
        except ClienteCorredorNoEncontradoException as e:
            # Relanzar con un mensaje más descriptivo
            raise ClienteCorredorNoEncontradoException(
                command.cliente_id, command.corredor_numero_antiguo
            ) from e
        except ClienteCorredorAsignacionDuplicadaException as e:
            # Relanzar con un mensaje más descriptivo
            raise ClienteCorredorAsignacionDuplicadaException(
                command.cliente_id, command.corredor_numero_nuevo
            ) from e
        except FechaAsignacionInvalidaException as e:
            # Relanzar la excepción de fecha inválida
            raise FechaAsignacionInvalidaException(str(fecha_asignacion)) from e


class EliminarAsignacionClienteCorredorUseCase:
    """Caso de uso para eliminar la asignación de un cliente a un corredor."""
    
    def __init__(self, cliente_corredor_repository):
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, cliente_id: UUID, corredor_numero: int) -> bool:
        """
        Elimina la asignación de un cliente a un corredor.
        
        Args:
            cliente_id: ID del cliente
            corredor_numero: Número del corredor
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
            
        Raises:
            ClienteCorredorNoEncontradoException: Si no existe la asignación
        """
        # Verificar que existe una asignación para el cliente y el corredor
        existing = self.cliente_corredor_repository.get_by_cliente_corredor(cliente_id, corredor_numero)
        if not existing:
            raise ClienteCorredorNoEncontradoException(cliente_id, corredor_numero)
        
        # Eliminar la asignación
        return self.cliente_corredor_repository.remove(cliente_id, corredor_numero)


class ListarClientesPorCorredorUseCase:
    """Caso de uso para listar todos los clientes asignados a un corredor."""
    
    def __init__(self, cliente_corredor_repository):
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, corredor_numero: int) -> List[ClienteCorredorDto]:
        """
        Lista todos los clientes asignados a un corredor.
        
        Args:
            corredor_numero: Número del corredor
            
        Returns:
            List[ClienteCorredorDto]: Lista de DTOs con las asignaciones
            
        Note:
            Si no hay asignaciones, devuelve una lista vacía
        """
        asignaciones = self.cliente_corredor_repository.get_by_corredor(corredor_numero)
        return [
            ClienteCorredorDto(
                cliente_id=asignacion.cliente_id,
                corredor_numero=asignacion.corredor_numero,
                fecha_asignacion=asignacion.fecha_asignacion
            )
            for asignacion in asignaciones
        ]


class ListarCorredoresPorClienteUseCase:
    """Caso de uso para listar todos los corredores asignados a un cliente."""
    
    def __init__(self, cliente_corredor_repository):
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, cliente_id: UUID) -> List[ClienteCorredorDto]:
        """
        Lista todos los corredores asignados a un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            List[ClienteCorredorDto]: Lista de DTOs con las asignaciones
            
        Note:
            Si no hay asignaciones, devuelve una lista vacía
        """
        asignaciones = self.cliente_corredor_repository.get_by_cliente(cliente_id)
        return [
            ClienteCorredorDto(
                cliente_id=asignacion.cliente_id,
                corredor_numero=asignacion.corredor_numero,
                fecha_asignacion=asignacion.fecha_asignacion
            )
            for asignacion in asignaciones
        ]
