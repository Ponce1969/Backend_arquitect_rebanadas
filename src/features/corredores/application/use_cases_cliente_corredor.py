from datetime import date
from uuid import UUID

from src.features.corredores.application.dtos_cliente_corredor import (
    ClienteCorredorDto,
    AsignarClienteCorredorCommand,
    ReasignarClienteCommand
)


class AsignarClienteCorredorUseCase:
    """Caso de uso para asignar un cliente a un corredor."""
    
    def __init__(self, cliente_repository, corredor_repository, cliente_corredor_repository):
        self.cliente_repository = cliente_repository
        self.corredor_repository = corredor_repository
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, command: AsignarClienteCorredorCommand) -> ClienteCorredorDto:
        """Asigna un cliente a un corredor."""
        # Verificar que el cliente existe
        cliente = self.cliente_repository.get_by_id(command.cliente_id)
        if not cliente:
            raise ValueError(f"No se encontró un cliente con ID {command.cliente_id}")
        
        # Verificar que el corredor existe
        corredor = self.corredor_repository.get_by_numero(command.corredor_numero)
        if not corredor:
            raise ValueError(f"No se encontró un corredor con número {command.corredor_numero}")
        
        # Verificar si ya existe una asignación para este cliente y corredor
        existing = self.cliente_corredor_repository.get_by_cliente_corredor(
            command.cliente_id, command.corredor_numero
        )
        if existing:
            raise ValueError(f"El cliente ya está asignado al corredor {command.corredor_numero}")
        
        # Crear la fecha de asignación si no se proporcionó
        fecha_asignacion = command.fecha_asignacion or date.today()
        
        # Crear la asignación
        asignacion = self.cliente_corredor_repository.add(
            command.cliente_id, command.corredor_numero, fecha_asignacion
        )
        
        return ClienteCorredorDto(
            cliente_id=asignacion.cliente_id,
            corredor_numero=asignacion.corredor_numero,
            fecha_asignacion=asignacion.fecha_asignacion
        )


class ReasignarClienteUseCase:
    """Caso de uso para reasignar un cliente de un corredor a otro."""
    
    def __init__(self, cliente_repository, corredor_repository, cliente_corredor_repository):
        self.cliente_repository = cliente_repository
        self.corredor_repository = corredor_repository
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, command: ReasignarClienteCommand) -> ClienteCorredorDto:
        """Reasigna un cliente de un corredor a otro."""
        # Verificar que el cliente existe
        cliente = self.cliente_repository.get_by_id(command.cliente_id)
        if not cliente:
            raise ValueError(f"No se encontró un cliente con ID {command.cliente_id}")
        
        # Verificar que el corredor antiguo existe
        corredor_antiguo = self.corredor_repository.get_by_numero(command.corredor_numero_antiguo)
        if not corredor_antiguo:
            raise ValueError(f"No se encontró un corredor con número {command.corredor_numero_antiguo}")
        
        # Verificar que el nuevo corredor existe
        corredor_nuevo = self.corredor_repository.get_by_numero(command.corredor_numero_nuevo)
        if not corredor_nuevo:
            raise ValueError(f"No se encontró un corredor con número {command.corredor_numero_nuevo}")
        
        # Verificar que existe una asignación para el cliente y el corredor antiguo
        existing = self.cliente_corredor_repository.get_by_cliente_corredor(
            command.cliente_id, command.corredor_numero_antiguo
        )
        if not existing:
            raise ValueError(f"El cliente no está asignado al corredor {command.corredor_numero_antiguo}")
        
        # Verificar que no existe una asignación para el cliente y el nuevo corredor
        existing_new = self.cliente_corredor_repository.get_by_cliente_corredor(
            command.cliente_id, command.corredor_numero_nuevo
        )
        if existing_new:
            raise ValueError(f"El cliente ya está asignado al corredor {command.corredor_numero_nuevo}")
        
        # Eliminar la asignación antigua
        self.cliente_corredor_repository.delete(command.cliente_id, command.corredor_numero_antiguo)
        
        # Crear la fecha de asignación si no se proporcionó
        fecha_asignacion = command.fecha_asignacion or date.today()
        
        # Crear la nueva asignación
        asignacion = self.cliente_corredor_repository.add(
            command.cliente_id, command.corredor_numero_nuevo, fecha_asignacion
        )
        
        return ClienteCorredorDto(
            cliente_id=asignacion.cliente_id,
            corredor_numero=asignacion.corredor_numero,
            fecha_asignacion=asignacion.fecha_asignacion
        )


class EliminarAsignacionClienteCorredorUseCase:
    """Caso de uso para eliminar la asignación de un cliente a un corredor."""
    
    def __init__(self, cliente_corredor_repository):
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, cliente_id: UUID, corredor_numero: int) -> bool:
        """Elimina la asignación de un cliente a un corredor."""
        # Verificar que existe una asignación para el cliente y el corredor
        existing = self.cliente_corredor_repository.get_by_cliente_corredor(cliente_id, corredor_numero)
        if not existing:
            raise ValueError(f"El cliente no está asignado al corredor {corredor_numero}")
        
        # Eliminar la asignación
        return self.cliente_corredor_repository.delete(cliente_id, corredor_numero)


class ListarClientesPorCorredorUseCase:
    """Caso de uso para listar todos los clientes asignados a un corredor."""
    
    def __init__(self, cliente_corredor_repository):
        self.cliente_corredor_repository = cliente_corredor_repository
    
    def execute(self, corredor_numero: int) -> list[ClienteCorredorDto]:
        """Lista todos los clientes asignados a un corredor."""
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
    
    def execute(self, cliente_id: UUID) -> list[ClienteCorredorDto]:
        """Lista todos los corredores asignados a un cliente."""
        asignaciones = self.cliente_corredor_repository.get_by_cliente(cliente_id)
        return [
            ClienteCorredorDto(
                cliente_id=asignacion.cliente_id,
                corredor_numero=asignacion.corredor_numero,
                fecha_asignacion=asignacion.fecha_asignacion
            )
            for asignacion in asignaciones
        ]
